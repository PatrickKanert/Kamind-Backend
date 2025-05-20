from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from tasks_app.models import Task, Comment
from .serializers import TaskListSerializer, TaskSerializer, CommentSerializer
from boards_app.models import Board

class AssignedTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

class ReviewingTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskListSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.created_by != request.user and task.board.owner != request.user:
            return Response({'detail': 'Nicht erlaubt'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class TaskCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comments = task.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        content = request.data.get('content')
        if not content:
            return Response({'detail': 'Content ist erforderlich.'}, status=400)
        comment = Comment.objects.create(task=task, author=request.user, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=201)

class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, task_id=task_id)
        if comment.author != request.user:
            return Response({'detail': 'Nicht erlaubt'}, status=403)
        comment.delete()
        return Response(status=204)
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from tasks_app.models import Task, Comment
from .serializers import TaskListSerializer, TaskSerializer, CommentSerializer

# 🔹 View to list all tasks assigned to the current user
class AssignedTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Returns all tasks where the current user is the assignee.
        """
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)


# 🔹 View to list all tasks where the current user is the reviewer
class ReviewingTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Returns all tasks where the current user is the reviewer.
        """
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)


# 🔹 Full CRUD ViewSet for tasks
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns all tasks. Access is filtered in get_object().
        """
        return Task.objects.all()

    def get_serializer_class(self):
        """
        Use a short serializer for list/retrieve,
        and a full serializer for create/update.
        """
        if self.action in ['list', 'retrieve']:
            return TaskListSerializer
        return TaskSerializer
    
    def get_object(self):
        """
        Returns a single task if the user is allowed to access it.
        Allowed roles: creator, board owner, or board member.
        """
        obj = super().get_object()
        user = self.request.user
        board = obj.board

        if not (
            obj.created_by == user or
            board.owner == user or
            user in board.members.all()
        ):
            raise PermissionDenied("You do not have permission to access this task.")
        return obj

    def perform_create(self, serializer):
        """
        Assigns the current user as the creator of the task.
        """
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Only the creator or the board owner may delete the task.
        """
        task = self.get_object()
        if task.created_by != request.user and task.board.owner != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


# 🔹 Handles GET and POST for comments on a task
class TaskCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        """
        Returns all comments for a given task.
        Only allowed if user has access to the board.
        """
        task = get_object_or_404(Task, id=task_id)
        user = request.user
        board = task.board

        if not (
            task.created_by == user or
            board.owner == user or
            user in board.members.all()
        ):
            raise PermissionDenied("You do not have permission to view comments on this task.")

        comments = task.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_id):
        """
        Adds a comment to the task.
        Only allowed if user is related to the board or task.
        """
        task = get_object_or_404(Task, id=task_id)
        user = request.user
        board = task.board

        if not (
            task.created_by == user or
            board.owner == user or
            user in board.members.all()
        ):
            raise PermissionDenied("You do not have permission to comment on this task.")

        content = request.data.get('content')
        if not content:
            return Response({'detail': 'Content is required.'}, status=400)

        comment = Comment.objects.create(task=task, author=user, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=201)


# 🔹 Handles deletion of a specific comment
class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        """
        Deletes a comment.
        Only the comment author is allowed to perform this action.
        """
        comment = get_object_or_404(Comment, id=comment_id, task_id=task_id)
        if comment.author != request.user:
            return Response({'detail': 'Not allowed'}, status=403)

        comment.delete()
        return Response(status=204)

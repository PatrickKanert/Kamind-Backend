from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, AssignedTasksView, ReviewingTasksView, TaskCommentView, CommentDeleteView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('tasks/assigned-to-me/', AssignedTasksView.as_view()),
    path('tasks/reviewing/', ReviewingTasksView.as_view()),
    path('tasks/<int:task_id>/comments/', TaskCommentView.as_view()),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDeleteView.as_view()),
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TaskViewSet,
    AssignedTasksView,
    ReviewingTasksView,
    TaskCommentView,
    CommentDeleteView
)

# Initialize DRF router for automatic route generation from TaskViewSet
router = DefaultRouter()

# Registers standard RESTful routes for TaskViewSet under the 'tasks/' endpoint
# Includes:
# - GET    /tasks/           → list all tasks
# - POST   /tasks/           → create a new task
# - GET    /tasks/{id}/      → retrieve a task
# - PATCH  /tasks/{id}/      → update a task
# - DELETE /tasks/{id}/      → delete a task
router.register(r'tasks', TaskViewSet, basename='tasks')

# Explicit URL patterns for custom task endpoints
urlpatterns = [
    # 🔹 Get all tasks assigned to the current user
    path('tasks/assigned-to-me/', AssignedTasksView.as_view()),

    # 🔹 Get all tasks where the current user is the reviewer
    path('tasks/reviewing/', ReviewingTasksView.as_view()),

    # 🔹 List or create comments for a specific task
    path('tasks/<int:task_id>/comments/', TaskCommentView.as_view()),

    # 🔹 Delete a specific comment by ID for a given task
    path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDeleteView.as_view()),

    # 🔹 Include the router-generated CRUD routes for tasks
    path('', include(router.urls)),
]

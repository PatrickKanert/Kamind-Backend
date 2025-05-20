from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignedTasksView, TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('tasks/assigned-to-me/', AssignedTasksView.as_view(), name='assigned-tasks'),
    path('', include(router.urls)),
]

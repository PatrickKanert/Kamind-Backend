from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet

# Initialize the DRF router to automatically generate RESTful routes
router = DefaultRouter()

# Register the BoardViewSet with the router under the 'boards/' path
# This creates endpoints like:
# - GET /boards/           → list all boards
# - POST /boards/          → create a new board
# - GET /boards/{id}/      → retrieve a specific board
# - PATCH /boards/{id}/    → update a board
# - DELETE /boards/{id}/   → delete a board
router.register(r'boards', BoardViewSet, basename='boards')

# Include the router-generated routes into the main urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Mounts all board endpoints under the root path
]

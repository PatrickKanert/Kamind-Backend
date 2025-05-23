from django.urls import path
from .views import RegistrationView, LoginView, EmailCheckView

# 🔹 URL patterns for authentication and user management
urlpatterns = [
    # 🔐 User Registration
    # Endpoint: POST /api/registration/
    # Description: Registers a new user and returns an auth token
    path('registration/', RegistrationView.as_view(), name='registration'),

    # 🔑 User Login
    # Endpoint: POST /api/login/
    # Description: Authenticates a user and returns an auth token
    path('login/', LoginView.as_view(), name='login'),

    # 📧 Email Existence Check
    # Endpoint: GET /api/email-check/?email=...
    # Description: Checks if a user with the given email exists
    # Requires authentication
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, LoginSerializer, UserShortSerializer
from auth_app.models import User

# 🔹 View for user registration (public access)
class RegistrationView(APIView):
    permission_classes = []  # No authentication required

    def post(self, request):
        """
        Registers a new user and returns an authentication token along with basic user info.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": user.fullname,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 View for user login (public access)
class LoginView(APIView):
    permission_classes = []  # No authentication required

    def post(self, request):
        """
        Authenticates a user and returns an authentication token along with user info.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": user.fullname,
                "email": user.email,
                "user_id": user.id
            })
        
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Authenticated view to check if an email is already registered
class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]  # Requires valid token

    def get(self, request):
        """
        Returns basic user data if a user with the given email exists.
        Only available to authenticated users.
        """
        email = request.query_params.get('email')
        if not email:
            return Response(
                {"detail": "Email parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            serializer = UserShortSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

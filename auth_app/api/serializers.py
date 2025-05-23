from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

# Get the custom user model
User = get_user_model()

# 🔹 Serializer for user registration
class RegistrationSerializer(serializers.ModelSerializer):
    # Confirm password field (not stored in DB)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True},  # Don't expose password in output
        }

    def validate(self, attrs):
        """
        Ensure that both password fields match.
        """
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        """
        Create a new user:
        - Encrypt password
        - Automatically generate a unique username based on email prefix
        """
        validated_data.pop('repeated_password')  # Remove unused field
        validated_data['password'] = make_password(validated_data['password'])

        email = validated_data.get('email')
        base_username = email.split('@')[0]  # Use the part before @ as base username
        username = base_username
        counter = 1

        # Ensure username uniqueness by appending a number if necessary
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base_username}{counter}"

        validated_data['username'] = username

        return User.objects.create(**validated_data)


# 🔹 Serializer for user login (email + password)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Authenticate user using email and password.
        """
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        data['user'] = user
        return data


# 🔹 Compact serializer used for user previews (e.g. board members)
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

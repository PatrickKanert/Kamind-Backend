from django.db import models
from django.contrib.auth.models import AbstractUser

# 🔹 Custom user model extending Django's AbstractUser
class User(AbstractUser):
    """
    Custom user model that uses email as the unique identifier
    instead of username. Adds a 'fullname' field.
    """

    # Full name of the user (used instead of first_name + last_name)
    fullname = models.CharField(
        max_length=150,
        help_text="The user's full name (e.g. John Doe)."
    )

    # Email address used as the primary identifier (must be unique)
    email = models.EmailField(
        unique=True,
        help_text="The user's unique email address (used for login)."
    )

    # Use email instead of username for login authentication
    USERNAME_FIELD = 'email'

    # Required fields when creating a user via createsuperuser or shell
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        """
        Human-readable representation of the user (their email address).
        """
        return self.email

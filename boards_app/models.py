from django.db import models
from django.conf import settings

class Board(models.Model):
    """
    Represents a collaborative board where users can manage and assign tasks.
    Each board has a title, an optional description, a creation timestamp,
    a single owner, and multiple members.
    """

    title = models.CharField(
        max_length=255,
        help_text="The name or title of the board"
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description for the board"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of when the board was created"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_boards',
        help_text="User who created and owns the board"
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='boards',
        blank=True,
        help_text="Users who have access to the board (excluding the owner)"
    )

    def __str__(self):
        """
        Returns a human-readable representation of the board.
        """
        return self.title

from django.db import models
from django.conf import settings
from boards_app.models import Board
from datetime import date

# Helper function for default due_date value
def default_due_date():
    """
    Sets the default due date to today's date.
    """
    return date.today().isoformat()

# 🔹 Task model for tracking work items within a board
class Task(models.Model):
    """
    Represents a task on a board, which can be assigned to a user and reviewed by another.
    Tasks include status, priority, due date, and metadata like creator and assignee.
    """

    # Task status options
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    # Task priority options
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # The board this task belongs to
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="The board this task is associated with."
    )

    # Title of the task
    title = models.CharField(
        max_length=255,
        help_text="A short, descriptive title for the task."
    )

    # Optional detailed description of the task
    description = models.TextField(
        blank=True,
        help_text="Additional details about the task."
    )

    # Current progress status of the task
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='to-do',
        help_text="The current status of the task."
    )

    # Priority level of the task
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="The urgency or importance of the task."
    )

    # Optional assignee (user responsible for executing the task)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        help_text="User assigned to execute the task (optional)."
    )

    # Reviewer (user responsible for checking or approving the task)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_tasks',
        help_text="User responsible for reviewing the task (required)."
    )

    # Due date for the task
    due_date = models.DateField(
        null=True,
        blank=True,
        default=default_due_date,
        help_text="The deadline by which the task should be completed."
    )

    # Creator of the task (usually the logged-in user who created it)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        help_text="User who created the task."
    )

    def __str__(self):
        """
        Human-readable string representation of the task.
        """
        return self.title


# 🔹 Comment model for storing task-related user discussions
class Comment(models.Model):
    """
    Represents a comment made by a user on a specific task.
    """

    # The task this comment is linked to
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The task this comment is associated with."
    )

    # Author of the comment
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="The user who wrote the comment."
    )

    # Text content of the comment
    content = models.TextField(
        help_text="The comment message body."
    )

    # Timestamp when the comment was created
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The time and date when the comment was posted."
    )

    def __str__(self):
        """
        Human-readable string representation of the comment.
        Shows the author's name and the task ID.
        """
        return f"Comment by {self.author.fullname} on Task {self.task.id}"

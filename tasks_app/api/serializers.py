from rest_framework import serializers
from tasks_app.models import Task, Comment
from auth_app.api.serializers import UserShortSerializer
from django.contrib.auth import get_user_model

# Use the custom user model
User = get_user_model()

# Read-only task serializer used for listing and retrieving tasks
class TaskListSerializer(serializers.ModelSerializer):
    # Full user object of the assignee
    assignee = UserShortSerializer()

    # Full user object of the reviewer (can be null)
    reviewer = UserShortSerializer(allow_null=True)

    # Computed field: number of comments linked to the task
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Return the number of comments associated with the task."""
        return obj.comments.count()


# Full task serializer used for creating and updating tasks
class TaskSerializer(serializers.ModelSerializer):
    # Write-only IDs for assigning users on creation/update
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(write_only=True, required=False)

    # Read-only user objects for output
    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)

    # Comment count as read-only field
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee_id', 'reviewer_id',
            'assignee', 'reviewer',
            'due_date', 'comments_count',
        ]

    def get_comments_count(self, obj):
        """Return the number of comments for the task."""
        return obj.comments.count()

    def create(self, validated_data):
        """
        Create a task with assigned assignee and reviewer users (if provided).
        The currently authenticated user is set as the creator.
        """
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        validated_data['assignee'] = User.objects.get(id=assignee_id) if assignee_id else None
        validated_data['reviewer'] = User.objects.get(id=reviewer_id) if reviewer_id else None
        validated_data['created_by'] = self.context['request'].user

        task = super().create(validated_data)
        return task

    def update(self, instance, validated_data):
        """
        Update a task's fields. The board field is immutable.
        Assignee and reviewer can be reassigned if IDs are provided.
        """
        validated_data.pop('board', None)  # board must not be updated

        if 'assignee_id' in self.initial_data:
            assignee_id = validated_data.pop('assignee_id', None)
            instance.assignee = User.objects.get(id=assignee_id) if assignee_id else None

        if 'reviewer_id' in self.initial_data:
            reviewer_id = validated_data.pop('reviewer_id', None)
            instance.reviewer = User.objects.get(id=reviewer_id) if reviewer_id else None

        return super().update(instance, validated_data)

    def validate(self, attrs):
        """
        Ensure that reviewer_id is provided when creating a task.
        """
        if self.instance is None and not self.initial_data.get('reviewer_id'):
            raise serializers.ValidationError({'reviewer_id': 'This field is required.'})
        return attrs


# Serializer for task comments
class CommentSerializer(serializers.ModelSerializer):
    # Return only the author's full name instead of a full object
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        """Return the full name of the comment's author."""
        return obj.author.fullname

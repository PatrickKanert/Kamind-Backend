from rest_framework import serializers
from tasks_app.models import Task
from auth_app.api.serializers import UserShortSerializer



class TaskListSerializer(serializers.ModelSerializer):
    assignee = UserShortSerializer()
    reviewer = UserShortSerializer(allow_null=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count() if hasattr(obj, 'comments') else 0


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee', 'reviewer', 'due_date'
        ]

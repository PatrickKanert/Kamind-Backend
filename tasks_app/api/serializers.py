from rest_framework import serializers
from tasks_app.models import Task, Comment
from auth_app.api.serializers import UserShortSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

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
        return obj.comments.count()


class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(write_only=True, required=False)
    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee_id', 'reviewer_id',
            'assignee', 'reviewer',
            'due_date', 'comments_count',
        ]

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        validated_data['assignee'] = User.objects.get(id=assignee_id) if assignee_id else None
        validated_data['reviewer'] = User.objects.get(id=reviewer_id) if reviewer_id else None

        validated_data['created_by'] = self.context['request'].user
        
        task = super().create(validated_data)
        
        return task

    def update(self, instance, validated_data):
        validated_data.pop('board', None)

        if 'assignee_id' in self.initial_data:
            assignee_id = validated_data.pop('assignee_id', None)
            instance.assignee = User.objects.get(id=assignee_id) if assignee_id else None

        if 'reviewer_id' in self.initial_data:
            reviewer_id = validated_data.pop('reviewer_id', None)
            instance.reviewer = User.objects.get(id=reviewer_id) if reviewer_id else None

        return super().update(instance, validated_data)

    def validate(self, attrs):
        if self.instance is None and not self.initial_data.get('reviewer_id'):
            raise serializers.ValidationError({'reviewer_id': 'Dieses Feld ist erforderlich.'})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        return obj.author.fullname

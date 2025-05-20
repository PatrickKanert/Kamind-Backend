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
    reviewer_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee_id', 'reviewer_id', 'due_date'
        ]
        read_only_fields = ['assignee', 'reviewer']

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        if assignee_id is not None:
            validated_data['assignee'] = User.objects.get(id=assignee_id)
        else:
            validated_data['assignee'] = None
        if reviewer_id is not None:
            validated_data['reviewer'] = User.objects.get(id=reviewer_id)

        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('board', None)
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        if assignee_id is not None:
            instance.assignee = User.objects.get(id=assignee_id)
        elif 'assignee_id' in self.initial_data:
            instance.assignee = None

        if reviewer_id is not None:
            instance.reviewer = User.objects.get(id=reviewer_id)
        elif 'reviewer_id' in self.initial_data:
            instance.reviewer = None

        return super().update(instance, validated_data)
    
    def validate(self, attrs):
        if not self.initial_data.get('reviewer_id'):
            raise serializers.ValidationError({'reviewer_id': 'Dieses Feld ist erforderlich.'})
        return attrs

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        return obj.author.fullname

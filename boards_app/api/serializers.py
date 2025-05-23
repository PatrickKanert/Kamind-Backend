from rest_framework import serializers
from boards_app.models import Board
from auth_app.models import User
from tasks_app.models import Task
from tasks_app.api.serializers import TaskListSerializer  

# Reusable short user serializer (id, email, fullname only)
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

# Detailed serializer for retrieving a full board view with members and tasks
class BoardDetailSerializer(serializers.ModelSerializer):
    # ID of the board owner (for easy access in frontend)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    # Full user data of the board owner
    owner_data = UserShortSerializer(source='owner', read_only=True)

    # List of all board members as user objects
    members = UserShortSerializer(many=True, read_only=True)

    # List of all tasks belonging to the board
    tasks = TaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            'id',           # Unique board ID
            'title',        # Title of the board
            'owner_id',     # ID of the board owner (read-only)
            'owner_data',   # Full user object of the owner
            'members',      # List of user objects who are board members
            'tasks'         # List of related tasks
        ]

    # Optional helper methods (currently unused in this serializer)

    def get_member_count(self, obj):
        """Returns the number of members in the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Returns the total number of tasks (tickets) in the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Returns the number of tasks with status 'to-do'."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Returns the number of tasks marked as 'high' priority."""
        return obj.tasks.filter(priority='high').count()

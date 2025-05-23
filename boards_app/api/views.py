from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from auth_app.api.serializers import UserShortSerializer
from django.db import models

from boards_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer

# ViewSet for managing boards (list, create, retrieve, update, delete)
class BoardViewSet(viewsets.ModelViewSet):
    # Restrict access to authenticated users only
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
    # Return all boards so get_object() can handle permission checks manually
        return Board.objects.all()

    def get_serializer_class(self):
        """
        Choose the appropriate serializer based on the action:
        - For retrieve and update actions, use the detailed serializer.
        - For list and create actions, use the basic serializer.
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return BoardDetailSerializer
        return BoardSerializer

    def get_object(self):
        """
        Fetch a specific board and enforce access control.
        Only the board owner or its members are allowed access.
        """
        obj = super().get_object()
        user = self.request.user

        if obj.owner != user and user not in obj.members.all():
            raise PermissionDenied("You do not have permission to access this board.")
        return obj

    def perform_create(self, serializer):
        """
        Create a new board:
        - Assign the current user as the owner.
        - Set members from the provided 'members' list.
        """
        board = serializer.save(owner=self.request.user)
        members = self.request.data.get('members', [])
        board.members.set(members)

    def update(self, request, *args, **kwargs):
        """
        Update an existing board.
        - Update the members list if included in the request.
        - Return the updated board data.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Only update members if they are provided in the request
        if 'members' in request.data:
            members = request.data['members']
            instance.members.set(members)

        return Response({
            "id": instance.id,
            "title": instance.title,
            "owner_data": UserShortSerializer(instance.owner).data,
            "members_data": UserShortSerializer(instance.members.all(), many=True).data,
        })
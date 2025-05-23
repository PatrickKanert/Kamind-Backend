from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db import models

from boards_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer

class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            models.Q(owner=user) | models.Q(members=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return BoardDetailSerializer
        return BoardSerializer

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj.owner != user and user not in obj.members.all():
            raise PermissionDenied("You do not have permission to access this board.")
        return obj

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        members = self.request.data.get('members', [])
        board.members.set(members)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if 'members' in request.data:
            members = request.data['members']
            instance.members.set(members)

        return Response(serializer.data)

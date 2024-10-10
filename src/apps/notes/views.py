from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from src.apps.notes.models import Note, Tag
from src.apps.notes.serializers import (
    NoteSerializer,
    CreateUpdateNoteSerializer,
    TagSerializer,
)

# TODO: Add ViewSet for tags


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUpdateNoteSerializer
        if self.action == "update":
            return CreateUpdateNoteSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="tags")
    def add_tags(self, request, pk=None):
        """
        Add tag to note
        """
        note = self.get_object()
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            tag = serializer.save(user=request.user)
            note.tags.add(tag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_tags.mapping.delete
    def remove_tags(self, request, pk=None):
        """
        Remove tag from note
        """
        tag_id = request.query_params.get("tag_id")
        note = self.get_object()
        tag = get_object_or_404(Tag, id=tag_id)
        note.tags.remove(tag)

        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.apps.notes.models import Note
from src.apps.notes.serializers import NoteSerializer, CreateUpdateNoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user.id)
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUpdateNoteSerializer
        if self.action == "update":
            return CreateUpdateNoteSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

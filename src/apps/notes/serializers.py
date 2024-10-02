from rest_framework import serializers

from src.apps.notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class CreateUpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "title",
            "content",
        )

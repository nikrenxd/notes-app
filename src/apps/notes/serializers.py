from rest_framework import serializers

from src.apps.notes.models import Note
from src.apps.tags.serializers import TagSerializer


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = (
            "id",
            "user",
            "title",
            "content",
            "tags",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")


class NoteAddTagsSerializer(serializers.Serializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=16),
        min_length=1,
        max_length=6,
    )


class NoteTagNameQuerySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=16)

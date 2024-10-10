from rest_framework import serializers

from src.apps.notes.models import Note, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        fields = (
            "id",
            "user",
            "title",
            "tags",
            "content",
            "created_at",
            "updated_at",
        )


class CreateUpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "title",
            "content",
        )

from rest_framework import serializers

from src.apps.tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)

    def validate_name(self, value: str):
        if len(value.split()) > 1:
            raise serializers.ValidationError("Tags must not contain spaces")
        return value

from django.db.models import QuerySet

from src.apps.notes.models import Note
from src.apps.tags.models import Tag
from src.apps.users.models import CustomUser


class NoteService:
    @staticmethod
    def get_existing_tags(
        user: CustomUser,
        validated_tags: list[str],
    ) -> tuple[QuerySet[Tag], list[str]]:
        """Search for tags in db"""
        tags = Tag.objects.filter(user=user, name__in=validated_tags)
        return tags, list(tags.values_list("name", flat=True))

    @staticmethod
    def add_tags(
        user: CustomUser,
        note: Note,
        validated_tags: list[str],
        exist_qs: QuerySet[Tag],
        exist_list: list[str],
    ) -> None:
        """Add tags to note, and create them if they don't exist"""
        new_tags = [
            Tag(
                name=tag,
                user=user,
            )
            for tag in validated_tags
            if tag not in exist_list
        ]

        tags = Tag.objects.bulk_create(new_tags)
        note.tags.add(*exist_qs, *tags)

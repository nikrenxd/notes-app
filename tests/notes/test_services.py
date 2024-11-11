import pytest

from src.apps.notes.models import Note
from src.apps.notes.services import NoteService
from src.apps.tags.models import Tag


@pytest.mark.django_db
class TestNoteService:
    @pytest.mark.parametrize(
        "data_list",
        [
            (["tag1", "tag2"]),
            (["tag3"]),
        ],
    )
    def test_get_existing_tags_list(
        self,
        user,
        data_list: list[str],
    ):
        _, tags_list = NoteService.get_existing_tags(user, data_list)
        assert tags_list == data_list

    def test_add_tags(self, user):
        data = ["tag1", "tag5", "tag4"]
        note = Note.objects.first()
        tags_qs, tags_list = NoteService.get_existing_tags(user, data)

        NoteService.add_tags(user, note, data, tags_qs, tags_list)

        assert Tag.objects.filter(name="tag1").count() == 1
        assert note.tags.get(name="tag5")

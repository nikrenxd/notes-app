import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


User = get_user_model()


@pytest.mark.django_db
class TestNotesViewSetBase:
    base_url = reverse("notes-list")

    @staticmethod
    def _dynamic_url(note_id: int) -> str:
        return reverse("notes-detail", kwargs={"pk": note_id})

    def action_url(self, note_id: int) -> str:
        return self._dynamic_url(note_id) + "tags/"


class TestNotesViewSetRoutes(TestNotesViewSetBase):
    def test_notes_create(self, authenticated_client: APIClient, user: User):
        note_data = {
            "title": "Test Note",
            "content": "lorem",
            "user": user.id,
        }

        response = authenticated_client.post(self.base_url, data=note_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("title") == "Test Note"
        assert response.data.get("user") == user.id

    def test_notes_list(self, authenticated_client: APIClient):
        response = authenticated_client.get(self.base_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) != 0


class TestNotesViewSetIdRoutes(TestNotesViewSetBase):
    def test_notes_detail(self, authenticated_client: APIClient):
        response = authenticated_client.get(self._dynamic_url(1))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("id") == 1
        assert response.data.get("title") == "Math notes"

    def test_notes_update(self, authenticated_client: APIClient):
        new_data = {"title": "Updated title", "content": "Updated content"}
        response = authenticated_client.put(self._dynamic_url(1), data=new_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("id") == 1
        assert response.data.get("title") == "Updated title"
        assert response.data.get("content") == "Updated content"

    def test_notes_delete(self, authenticated_client):
        response = authenticated_client.delete(self._dynamic_url(1))

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestNotesViewSetActions(TestNotesViewSetBase):
    def test_notes_add_tags(self, authenticated_client: APIClient):
        tag_name = {"name": "tag3"}
        response = authenticated_client.post(
            self._dynamic_url(2) + "tags/", data=tag_name
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("name") == "tag3"

    def test_notes_remove_tags(self, authenticated_client: APIClient):
        query_param = "?tag_id=2"
        response = authenticated_client.delete(self.action_url(2) + query_param)

        assert response.status_code == status.HTTP_204_NO_CONTENT

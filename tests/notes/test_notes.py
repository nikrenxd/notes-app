import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from src.apps.tags.models import Tag
from tests.utils import TestsBase

User = get_user_model()


@pytest.mark.django_db
class TestNotesViewSet(TestsBase):
    base_url_name = "notes-list"
    detail_url_name = "notes-detail"

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

    def test_notes_list_filter(self, authenticated_client: APIClient):
        response = authenticated_client.get(
            self.base_url,
            query_params={"tag_names": "tag1"},
        )

        assert response.data[0].get("tags")[0].get("name") == "tag1"

    def test_notes_detail(self, authenticated_client: APIClient):
        response = authenticated_client.get(self.detail_url(1))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("id") == 1
        assert response.data.get("title") == "Math notes"

    def test_notes_update(self, authenticated_client: APIClient):
        new_data = {"title": "Updated title", "content": "Updated content"}
        response = authenticated_client.put(self.detail_url(1), data=new_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("id") == 1
        assert response.data.get("title") == "Updated title"
        assert response.data.get("content") == "Updated content"

    def test_notes_partial_update(self, authenticated_client: APIClient):
        new_data = {"content": "Updated content"}
        response = authenticated_client.patch(self.detail_url(1), data=new_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("content") == "Updated content"

    def test_notes_delete(self, authenticated_client):
        response = authenticated_client.delete(self.detail_url(1))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_notes_add_tags(self, authenticated_client: APIClient):
        tags = {"tags": ["tag1", "notexists"]}

        assert Tag.objects.filter(name="tag1").exists()
        assert not Tag.objects.filter(name="notexists").exists()

        response = authenticated_client.post(
            self.action_url(2, "tags"),
            data=tags,
        )

        assert Tag.objects.filter(name="notexists").exists()
        assert len(Tag.objects.filter(name="tag1")) == 1

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("tags")[0] == "tag1"
        assert response.data.get("tags")[1] == "notexists"

    def test_notes_remove_tags(self, authenticated_client: APIClient):
        response = authenticated_client.delete(
            self.action_url(2, "tags"),
            query_params={"tag_id": 2},
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

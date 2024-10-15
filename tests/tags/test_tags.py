import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from tests.utils import TestsBase

User = get_user_model()


@pytest.mark.django_db
class TestTagsViewSet(TestsBase):
    base_url_name = "tags-list"
    detail_url_name = "tags-detail"

    def test_tag_list(self, authenticated_client: APIClient, user: User):
        response = authenticated_client.get(self.base_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) != 0

    def test_tag_update(self, authenticated_client: APIClient):
        data = {"name": "updated "}
        response = authenticated_client.put(self.detail_url(1), data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("name") == "updated"

    def test_tag_delete(self, authenticated_client: APIClient):
        response = authenticated_client.delete(self.detail_url(1))

        assert response.status_code == status.HTTP_204_NO_CONTENT

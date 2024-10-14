import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
class TestUser:
    def test_register(self, api_client, user_credentials):
        register_url = reverse("user-create")

        response = api_client.post(register_url, data=user_credentials)

        assert response.status_code == 201

    def test_login(self, api_client, user_credentials):
        user_credentials.update({"email": "user@mail.com"})
        login_url = reverse("login")

        response = api_client.post(login_url, data=user_credentials)

        access_token = response.json().get("access")

        assert response.status_code == 200
        assert access_token is not None

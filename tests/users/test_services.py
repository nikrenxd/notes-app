from django.contrib.auth.hashers import check_password

from src.apps.users.services import UserService


def test_user_hash_password():
    plain_password = "1234"
    hash_password = UserService.user_hash_password("1234")

    assert hash_password != plain_password
    assert check_password(plain_password, hash_password)

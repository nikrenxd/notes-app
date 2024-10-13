from django.contrib.auth.hashers import make_password


class UserService:
    @staticmethod
    def user_hash_password(password: str) -> str:
        return make_password(password)

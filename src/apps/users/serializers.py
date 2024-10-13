from rest_framework import serializers

from src.apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ("email", "password")

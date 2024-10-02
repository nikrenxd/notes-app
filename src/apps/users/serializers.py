from rest_framework.serializers import ModelSerializer

from src.apps.users.models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        user.save()
        return user

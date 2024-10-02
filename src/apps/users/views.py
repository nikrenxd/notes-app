from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from src.apps.users.models import CustomUser
from src.apps.users.serializers import UserSerializer


class UserViewSet(GenericViewSet, CreateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

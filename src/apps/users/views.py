from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from src.apps.users.models import CustomUser
from src.apps.users.serializers import UserSerializer


@extend_schema(
    tags=["auth"],
)
class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

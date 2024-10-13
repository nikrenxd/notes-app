from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from src.apps.users.models import CustomUser
from src.apps.users.serializers import UserSerializer
from src.apps.users.services import UserService


@extend_schema(
    tags=["auth"],
)
class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        hashed_password = UserService.user_hash_password(
            serializer.validated_data["password"]
        )
        serializer.save(
            email=serializer.validated_data["email"],
            password=hashed_password,
        )

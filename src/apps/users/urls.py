from rest_framework.routers import SimpleRouter

from src.apps.users.views import UserViewSet

router = SimpleRouter()


router.register(r"users", UserViewSet, basename="users")

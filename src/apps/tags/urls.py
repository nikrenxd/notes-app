from rest_framework import routers

from src.apps.tags.views import TagViewSet

router = routers.SimpleRouter()

router.register(r"tags", TagViewSet, basename="tags")

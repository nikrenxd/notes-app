from rest_framework import routers

from src.apps.notes.views import NoteViewSet, TagViewSet

router = routers.SimpleRouter()

router.register(r"notes", NoteViewSet, basename="notes")
router.register(r"tags", TagViewSet, basename="tags")

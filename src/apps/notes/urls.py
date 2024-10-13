from rest_framework import routers

from src.apps.notes.views import NoteViewSet

router = routers.SimpleRouter()

router.register(r"notes", NoteViewSet, basename="notes")

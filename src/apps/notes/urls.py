from django.urls import path
from rest_framework import routers

from src.apps.notes.views import NoteViewSet, NoteRemoveTagView

router = routers.SimpleRouter()


router.register(r"notes", NoteViewSet, basename="notes")

urlpatterns = [
    path(
        "notes/<note_id>/tags/<tag_id>/",
        NoteRemoveTagView.as_view(),
        name="note-remove-tag",
    ),
]

urlpatterns += router.urls

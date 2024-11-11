from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.notes.filters import NoteFilter
from src.apps.notes.services import NoteService
from src.mixins import FilterQuerySetByUserMixin
from src.apps.notes.models import Note
from src.apps.notes.serializers import (
    NoteSerializer,
    NoteTagNameQuerySerializer,
    NoteAddTagsSerializer,
)
from src.permissions import OwnerPermission


class NoteViewSet(FilterQuerySetByUserMixin, viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (
        OwnerPermission,
        IsAuthenticated,
    )
    filterset_class = NoteFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            return queryset.prefetch_related("tags")

        return queryset

    def get_serializer_class(self):
        if self.action == "add_tags":
            return NoteAddTagsSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(request=NoteTagNameQuerySerializer)
    @action(detail=True, methods=["post"], url_path="tags")
    def add_tags(self, request: Request, pk: int | None = None):
        """Add tags to note"""
        user = request.user
        note = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data["tags"]

        # Get existing tags from db
        tags_qs, tags_list = NoteService.get_existing_tags(
            user=user,
            validated_tags=data,
        )

        NoteService.add_tags(
            user=user,
            note=note,
            validated_tags=data,
            exist_qs=tags_qs,
            exist_list=tags_list,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoteRemoveTagView(FilterQuerySetByUserMixin, GenericAPIView):
    queryset = Note.objects.prefetch_related("tags")
    permission_classes = (
        OwnerPermission,
        IsAuthenticated,
    )
    lookup_url_kwarg = "note_id"

    def delete(self, request, *args, **kwargs):
        tag_id = self.kwargs["tag_id"]
        note = self.get_object()

        tag = get_object_or_404(note.tags, id=tag_id)
        note.tags.remove(tag)

        return Response(status=status.HTTP_204_NO_CONTENT)

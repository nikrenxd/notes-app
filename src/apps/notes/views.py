from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.notes.exceptions import TagAddLimitException
from src.apps.notes.filters import NoteFilter
from src.mixins import FilterQuerySetByUserMixin
from src.apps.tags.models import Tag
from src.apps.notes.models import Note
from src.apps.notes.serializers import (
    NoteSerializer,
    TagSerializer,
    TagIdQuerySerializer,
    TagNameQuerySerializer,
)
from src.permissions import OwnerPermission


class NoteViewSet(FilterQuerySetByUserMixin, viewsets.ModelViewSet):
    queryset = Note.objects.prefetch_related("tags")
    serializer_class = NoteSerializer
    permission_classes = (
        OwnerPermission,
        IsAuthenticated,
    )
    filterset_class = NoteFilter

    def get_serializer_class(self):
        if self.action == "add_tags":
            return TagSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(request=TagNameQuerySerializer)
    @action(detail=True, methods=["post"], url_path="tags")
    def add_tags(self, request: Request, pk: int | None = None):
        """Add tag to note"""
        user = request.user
        data = request.data
        # Add multiple tags to note if array of json objects passed
        is_list = False
        if isinstance(request.data, list):
            is_list = True
        if is_list and not len(request.data) <= 6:
            raise TagAddLimitException

        note = self.get_object()
        serializer = self.get_serializer(data=data, many=is_list)

        serializer.is_valid(raise_exception=True)
        tag = serializer.save(user=user)

        if is_list:
            note.tags.add(*tag)
        else:
            note.tags.add(tag)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(parameters=[TagIdQuerySerializer])
    @add_tags.mapping.delete
    def remove_tags(self, request: Request, pk: int | None = None):
        """Remove tag from note"""
        tag_id = request.query_params.get("tag_id")
        note = self.get_object()

        tag = get_object_or_404(Tag, id=tag_id)
        note.tags.remove(tag)
        return Response(status=status.HTTP_204_NO_CONTENT)

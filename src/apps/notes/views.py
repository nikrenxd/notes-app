from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.notes.models import Note, Tag
from src.apps.notes.serializers import (
    NoteSerializer,
    TagSerializer,
    NoteCreateUpdateSerializer,
    TagQuerySerializer,
    TagAddToNoteSerializer,
)
from src.apps.notes.permissions import OwnerPermission


@extend_schema_view(partial_update=extend_schema(exclude=True))
class TagViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (
        OwnerPermission,
        IsAuthenticated,
    )

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (
        OwnerPermission,
        IsAuthenticated,
    )

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return NoteCreateUpdateSerializer
        if self.action == "update":
            return NoteCreateUpdateSerializer
        if self.action == "partial_update":
            return NoteCreateUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(request=TagAddToNoteSerializer)
    @action(detail=True, methods=["post"], url_path="tags")
    def add_tags(self, request: Request, pk: int | None = None):
        """
        Add tag to note
        """
        note = self.get_object()

        # Multiple multiple tags
        is_list = False
        if isinstance(request.data, list):
            is_list = True

        if len(request.data) > 6:
            return Response(
                {"detail": "You can add maximum 6 tags"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TagSerializer(data=request.data, many=is_list)

        if serializer.is_valid():
            tag = serializer.save(user=request.user)
            note.tags.add(*tag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[TagQuerySerializer])
    @add_tags.mapping.delete
    def remove_tags(self, request: Request, pk: int | None = None):
        """
        Remove tag from note
        """
        tag_id = request.query_params.get("tag_id")
        note = self.get_object()
        tag = get_object_or_404(Tag, id=tag_id)
        note.tags.remove(tag)

        return Response(status=status.HTTP_204_NO_CONTENT)

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from src.apps.tags.models import Tag
from src.apps.tags.serializers import TagSerializer
from src.mixins import FilterQuerySetByUserMixin
from src.permissions import OwnerPermission


@extend_schema_view(partial_update=extend_schema(exclude=True))
class TagViewSet(
    FilterQuerySetByUserMixin,
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

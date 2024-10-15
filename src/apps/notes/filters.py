from django.db.models import QuerySet
from django_filters import rest_framework as filters

from src.apps.notes.models import Note


class NoteFilter(filters.FilterSet):
    tag_names = filters.CharFilter(field_name="tags__name", method="filter_tag_names")

    def filter_tag_names(self, queryset: QuerySet, name: str, value: str):
        tags = value.split(",")
        return queryset.filter(tags__name__in=tags).distinct()

    class Meta:
        model = Note
        fields = ("tag_names",)

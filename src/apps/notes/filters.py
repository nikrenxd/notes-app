from django_filters import rest_framework as filters

from src.apps.notes.models import Note


class NoteFilter(filters.FilterSet):
    tag_name = filters.CharFilter(lookup_expr="icontains", field_name="tags__name")

    class Meta:
        model = Note
        fields = ("tag_name",)

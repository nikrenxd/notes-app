from django.db.models import QuerySet


class FilterQuerySetByUserMixin:
    def get_queryset(self):
        qs: QuerySet = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

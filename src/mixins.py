class FilterQuerySetByUserMixin:
    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs

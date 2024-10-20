import uuid

from rest_framework.reverse import reverse


class TestsBase:
    base_url_name = None
    detail_url_name = None

    @property
    def base_url(self, **kwargs):
        return reverse(self.base_url_name, kwargs=kwargs)

    def detail_url(
        self,
        identifier: int | str | uuid.UUID = None,
        identify_by: str = "pk",
        **kwargs,
    ) -> str:
        if identifier and identify_by:
            return reverse(self.detail_url_name, kwargs={identify_by: identifier})
        return reverse(self.detail_url_name, kwargs=kwargs)

    def action_url(
        self,
        identifier: int | str,
        action_name: str,
        identify_by: str = "pk",
    ) -> str:
        action_name += "/"
        return self.detail_url(identifier, identify_by) + action_name

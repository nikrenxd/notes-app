import uuid

from rest_framework.reverse import reverse


class TestsBase:
    base_url_name = None
    detail_url_name = None

    @property
    def base_url(self):
        return reverse(self.base_url_name)

    def detail_url(
        self,
        identifier: int | str | uuid.UUID,
        identify_by: str = "pk",
    ) -> str:
        return reverse(self.detail_url_name, kwargs={identify_by: identifier})

    def action_url(
        self,
        identifier: int | str,
        action_name: str,
        identify_by: str = "pk",
    ) -> str:
        action_name += "/"
        return self.detail_url(identifier, identify_by) + action_name

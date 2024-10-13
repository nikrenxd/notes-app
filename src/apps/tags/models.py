from django.db import models

from src.apps.notes.models import Note
from src.apps.users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=16)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    notes = models.ManyToManyField(Note, related_name="tags")

    def __str__(self):
        return f"#{self.name}"

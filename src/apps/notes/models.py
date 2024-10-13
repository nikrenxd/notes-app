from django.db import models

from src.apps.users.models import CustomUser


class Note(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.title}"

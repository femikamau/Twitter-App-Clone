import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.utils.models import TimeStampedModel

User = get_user_model()


class Post(TimeStampedModel):
    """
    Post model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="posts", blank=True)

    def __str__(self):
        return f"{self.user} - Post: {self.id}"

    class Meta:
        ordering = ["-created_at"]


class Comment(TimeStampedModel):
    """
    Comment model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user} - Comment: {self.id}"

    class Meta:
        ordering = ["-created_at"]

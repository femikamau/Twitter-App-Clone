from django.contrib.auth import get_user_model
from django.db import models

from apps.utils.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    """
    Profile model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"

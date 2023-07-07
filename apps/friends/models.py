from django.contrib.auth import get_user_model
from django.db import models

from apps.utils.models import TimeStampedModel

User = get_user_model()


class Friend(TimeStampedModel):
    from_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="following",
    )
    to_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    updated_at = None

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"

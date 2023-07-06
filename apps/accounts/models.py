from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.utils.models import TimeStampedModel

from .managers import CustomUserManager


class User(AbstractUser, TimeStampedModel):
    """
    Custom User Model
    """

    email = models.EmailField("email address", unique=True)
    first_name = models.CharField("first name", max_length=30, blank=False)
    last_name = models.CharField("last name", max_length=30, blank=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    # Override the objects attribute to use the CustomUserManager
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username

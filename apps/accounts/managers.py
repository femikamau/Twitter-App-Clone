from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom User Model Manager
    """

    def _create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields,
    ):
        """
        Create and save a User with the given username, email,
        first_name, last_name, and password.
        """

        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given email must be set")

        if not first_name:
            raise ValueError("The given first name must be set")

        if not last_name:
            raise ValueError("The given last name must be set")

        if not password:
            raise ValueError("The given password must be set")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields,
    ):
        """
        Create and save a regular User with the given username, email,
        first_name, last_name, and password.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if extra_fields.get("is_superuser") is True:
            raise ValueError("Regular users must not have is_superuser=True")

        return self._create_user(
            username,
            email,
            first_name,
            last_name,
            password,
            **extra_fields,
        )

    def create_superuser(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields,
    ):
        """
        Create and save a SuperUser with the given username, email,
        first_name, last_name, and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is False:
            raise ValueError("Superusers must have is_staff=True")

        if extra_fields.get("is_superuser") is False:
            raise ValueError("Superusers must have is_superuser=True")

        return self._create_user(
            username,
            email,
            first_name,
            last_name,
            password,
            **extra_fields,
        )

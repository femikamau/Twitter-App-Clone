from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CustomUserManagerTestCase(TestCase):
    def test_create_user(self):
        user_details = {
            "email": "testuser@email.com",
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "password": "testpass123",
        }

        user = User.objects.create_user(**user_details)

        # Get the user from the database
        user = User.objects.get(username="testuser")

        self.assertEqual(user.email, user.email)
        self.assertEqual(user.first_name, user.first_name)
        self.assertEqual(user.last_name, user.last_name)
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_user(**{**user_details, "email": None})

        with self.assertRaises(ValueError):
            User.objects.create_user(**{**user_details, "first_name": None})

        with self.assertRaises(ValueError):
            User.objects.create_user(**{**user_details, "last_name": None})

        with self.assertRaises(ValueError):
            User.objects.create_user(**{**user_details, "username": None})

        with self.assertRaises(ValueError):
            User.objects.create_user(**{**user_details, "password": None})

        with self.assertRaises(ValueError):
            User.objects.create_user(**{**user_details, "is_superuser": True})

    def test_create_superuser(self):
        superuser_details = {
            "email": "superuser@gmail.com",
            "first_name": "Super",
            "last_name": "User",
            "username": "superuser",
            "password": "testpass123",
        }

        superuser = User.objects.create_superuser(**superuser_details)

        # Get the user from the database
        superuser = User.objects.get(username="superuser")

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(**{**superuser_details, "is_staff": False})

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                **{**superuser_details, "is_superuser": False}
            )

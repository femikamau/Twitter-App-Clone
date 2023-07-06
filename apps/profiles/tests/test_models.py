from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.tests.factories import AccountFactory
from apps.profiles.models import Profile

User = get_user_model()


class ProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AccountFactory()

    def test_profile_creation(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        self.assertIsInstance(self.user.profile, Profile)
        self.assertEqual(
            str(Profile.objects.get(user=self.user)), f"{self.user.username}'s Profile"
        )

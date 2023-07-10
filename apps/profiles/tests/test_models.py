from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.tests.factories import AccountFactory
from apps.profiles.models import Profile

User = get_user_model()


class ProfileModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AccountFactory()

    def test_profile_instance(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertTrue(isinstance(self.user.profile, Profile))
        self.assertEqual(self.user.profile.__str__(), f"{self.user.username}'s Profile")

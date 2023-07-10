from django.test import TestCase

from apps.accounts.tests.factories import AccountFactory

from ..models import Profile


class ProfileSignalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AccountFactory()

    def test_profile_creation(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        self.assertIsInstance(self.user.profile, Profile)
        self.assertEqual(
            str(Profile.objects.get(user=self.user)), f"{self.user.username}'s Profile"
        )

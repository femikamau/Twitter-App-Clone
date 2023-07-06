from django.contrib.auth import get_user_model
from django.test import TestCase

from .factories import AccountFactory

User = get_user_model()


class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AccountFactory()

    def test_account_creation(self):
        testuser = User.objects.get(username=self.user.username)

        self.assertEqual(testuser.username, self.user.username)
        self.assertEqual(testuser.email, self.user.email)
        self.assertEqual(testuser.first_name, self.user.first_name)
        self.assertEqual(testuser.last_name, self.user.last_name)
        self.assertTrue(testuser.is_active)
        self.assertFalse(testuser.is_staff)
        self.assertFalse(testuser.is_superuser)
        self.assertEqual(str(testuser), self.user.username)

from django.test import TestCase

from ..models import Friend
from .factories import FriendFactory


class FriendModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.friend = FriendFactory()

    def test_friend_instance(self):
        self.assertEqual(Friend.objects.count(), 1)
        self.assertTrue(isinstance(self.friend, Friend))
        self.assertEqual(
            self.friend.__str__(), f"{self.friend.from_user} -> {self.friend.to_user}"
        )

    def test_friend_unique_together(self):
        with self.assertRaises(Exception):
            FriendFactory(
                from_user=self.friend.from_user,
                to_user=self.friend.to_user,
            )

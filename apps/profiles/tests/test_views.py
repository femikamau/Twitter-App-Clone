from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.tests.factories import AccountFactory
from apps.friends.tests.factories import FriendFactory
from apps.posts.tests.factories import PostFactory


class ProfileViewsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AccountFactory()
        cls.user2 = AccountFactory()
        cls.user3 = AccountFactory()

        cls.posts = PostFactory.create_batch(5, user=cls.user)
        cls.posts2 = PostFactory.create_batch(5, user=cls.user2)

    def test_read_profiles(self):
        url = reverse("profile-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_read_profile(self):
        url = reverse("profile-detail", args=[self.user.username])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["avatar"], None)
        self.assertEqual(response.data["bio"], "")
        self.assertEqual(response.data["followers"], 0)
        self.assertEqual(response.data["following"], 0)
        self.assertEqual(response.data["posts"], 5)

    def test_posts_action(self):
        url = reverse("profile-posts", args=[self.user.username])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

        # Test post creation from in user's own profile

        self.client.force_authenticate(user=self.user)

        url = reverse("profile-posts", args=[self.user.username])

        data = {
            "content": "Test post",
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], data["content"])

        # Test post creation from in another user's profile

        self.client.force_authenticate(user=self.user2)

        url = reverse("profile-posts", args=[self.user.username])

        data = {
            "content": "Test post",
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_and_unfollow_actions(self):
        # Follow Action

        url = reverse("profile-follow", args=[self.user.username])

        # Assert that a user can't follow themselves

        self.client.force_authenticate(user=self.user)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that a user can follow another user

        self.client.force_authenticate(user=self.user2)

        followers_before = self.user.followers.count()

        response = self.client.post(url)

        followers_after = self.user.followers.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(followers_after, followers_before + 1)
        self.assertEqual(
            response.data, {"detail": f"You are now following {self.user.username}"}
        )

        # Assert that a user can't follow another user twice

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Unfollow Action

        url = reverse("profile-unfollow", args=[self.user.username])

        # Assert that a user cannot unfollow themselves

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that a user can unfollow another user

        self.client.force_authenticate(user=self.user2)

        followers_before = self.user.followers.count()

        response = self.client.delete(url)

        followers_after = self.user.followers.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(followers_after, followers_before - 1)

        # Assert that a user can't unfollow another user twice

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_followers_and_following_action(self):
        FriendFactory(from_user=self.user, to_user=self.user2)
        FriendFactory(from_user=self.user, to_user=self.user3)
        FriendFactory(from_user=self.user2, to_user=self.user3)
        FriendFactory(from_user=self.user3, to_user=self.user2)

        url = reverse("profile-followers", args=[self.user2.username])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        url = reverse("profile-following", args=[self.user.username])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

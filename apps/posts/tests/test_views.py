from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.tests.factories import AccountFactory
from apps.profiles.models import Profile

from ..serializers.posts import ReadPostSerializer
from .factories import CommentFactory, PostFactory


class PostViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = AccountFactory()
        cls.user2 = AccountFactory()

        cls.post = PostFactory(user=cls.user)
        cls.post2 = PostFactory(user=cls.user)

        CommentFactory.create_batch(5, user=cls.user, post=cls.post)
        CommentFactory.create_batch(5, user=cls.user, post=cls.post2)

        cls.profile = Profile.objects.get(user=cls.user)

    def test_post_instance(self):
        response = self.client.get(reverse("post-detail", args=[self.post.id]))

        serializer = ReadPostSerializer(
            self.post, context={"request": response.wsgi_request}
        )

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_update(self):
        # Only the owner of the post can update a post
        self.client.force_authenticate(user=self.user2)

        response = self.client.patch(
            reverse("post-detail", args=[self.post.id]),
            {"content": "Updated content"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse("post-detail", args=[self.post.id]),
            {"content": "Updated content"},
        )

        self.assertEqual(response.data["content"], "Updated content")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete(self):
        # Only the owner of the post can delete a post
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(reverse("post-detail", args=[self.post.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse("post-detail", args=[self.post.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

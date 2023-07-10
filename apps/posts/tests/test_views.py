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

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("post-comments", args=[self.post.id])

        response = self.client.post(
            url,
            data={"content": "Test Comment"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.comments.count(), 6)
        self.assertEqual(self.post.comments.first().content, "Test Comment")

    def test_read_comment(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("post-comments", args=[self.post.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.comments.count(), 5)

    def test_update_comment(self):
        # Assert that only the owner of the comment can update it

        self.client.force_authenticate(user=self.user2)

        url = reverse("comment-detail", args=[self.post.comments.first().id])

        response = self.client.patch(url, data={"content": "Updated Comment"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(url, data={"content": "Updated Comment"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self):
        # Assert that only the owner of the comment can delete it

        self.client.force_authenticate(user=self.user2)

        url = reverse("comment-detail", args=[self.post.comments.first().id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_like(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("post-like-post", args=[self.post.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.likes.count(), 1)

        #  Assert that a user can only like a post once

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.post.likes.count(), 1)

    def test_read_like(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("post-likes", args=[self.post.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.likes.count(), 0)

    def test_delete_like(self):
        self.client.force_authenticate(user=self.user)

        like_url = reverse("post-like-post", args=[self.post.id])

        unlike_url = reverse("post-unlike-post", args=[self.post.id])

        response = self.client.post(like_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.likes.count(), 1)

        response = self.client.delete(unlike_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.post.likes.count(), 0)

        # Assert that a user can only unlike a post once

        response = self.client.delete(unlike_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.post.likes.count(), 0)

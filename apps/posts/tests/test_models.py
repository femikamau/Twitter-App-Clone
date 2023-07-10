from django.test import TestCase

from apps.accounts.tests.factories import AccountFactory
from apps.posts.models import Comment, Like, Post


class PostModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = AccountFactory()

        cls.post = Post.objects.create(
            user=cls.user,
            content="Test content",
        )

    def test_post_creation(self):
        test_post = Post.objects.get(id=self.post.id)

        self.assertEqual(test_post.user, self.user)
        self.assertEqual(test_post.content, self.post.content)
        self.assertEqual(str(test_post), f"{self.user} - Post: {self.post.id}")

    def test_post_ordering(self):
        post2 = Post.objects.create(
            user=self.user,
            content="Test content 2",
        )

        self.assertEqual(Post.objects.first(), post2)
        self.assertEqual(Post.objects.last(), self.post)


class CommentModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = AccountFactory()

        cls.post = Post.objects.create(
            user=cls.user,
            content="Test content",
        )

        cls.comment = Comment.objects.create(
            user=cls.user,
            post=cls.post,
            content="Test comment",
        )

    def test_comment_creation(self):
        test_comment = Comment.objects.get(id=self.comment.id)

        self.assertEqual(test_comment.user, self.user)
        self.assertEqual(test_comment.post, self.post)
        self.assertEqual(test_comment.content, self.comment.content)
        self.assertEqual(str(test_comment), f"{self.user} - Comment: {self.comment.id}")

    def test_comment_ordering(self):
        comment2 = Comment.objects.create(
            user=self.user,
            post=self.post,
            content="Test comment 2",
        )

        self.assertEqual(Comment.objects.first(), comment2)
        self.assertEqual(Comment.objects.last(), self.comment)


class LikeModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = AccountFactory()
        cls.user2 = AccountFactory()

        cls.post = Post.objects.create(
            user=cls.user,
            content="Test content",
        )

        cls.like = Like.objects.create(
            user=cls.user,
            post=cls.post,
        )

    def test_like_creation(self):
        test_like = Like.objects.get(id=self.like.id)

        self.assertEqual(test_like.user, self.user)
        self.assertEqual(test_like.post, self.post)
        self.assertEqual(str(test_like), f"{self.user} - Like: {self.like.id}")

    def test_like_ordering(self):
        like2 = Like.objects.create(
            user=self.user2,
            post=self.post,
        )

        self.assertEqual(Like.objects.first(), like2)
        self.assertEqual(Like.objects.last(), self.like)

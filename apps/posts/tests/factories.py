import factory

from apps.accounts.tests.factories import AccountFactory

from ..models import Comment, Post


class PostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(AccountFactory)
    content = factory.Faker("text")

    class Meta:
        model = Post


class CommentFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(AccountFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker("text")

    class Meta:
        model = Comment

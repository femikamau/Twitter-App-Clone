import factory

from apps.accounts.tests.factories import AccountFactory

from ..models import Friend


class FriendFactory(factory.django.DjangoModelFactory):
    from_user = factory.SubFactory(AccountFactory)
    to_user = factory.SubFactory(AccountFactory)

    class Meta:
        model = Friend

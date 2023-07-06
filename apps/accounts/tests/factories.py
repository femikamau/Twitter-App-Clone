import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")

    class Meta:
        model = User

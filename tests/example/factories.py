import factory
from django.contrib.auth import get_user_model
from factory import fuzzy


# a factory.Factory class for creating Django users
# https://factoryboy.readthedocs.io/en/latest/reference.html#factory.django.DjangoModelFactory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    id = factory.Sequence(lambda n: n)  # noqa: A003
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: f"test_user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_active = fuzzy.FuzzyChoice([True, False])
    is_staff = fuzzy.FuzzyChoice([True, False])
    is_superuser = fuzzy.FuzzyChoice([True, False])


def create_fixtures(n):
    """Create n users."""
    return get_user_model().objects.bulk_create(UserFactory.create_batch(n))

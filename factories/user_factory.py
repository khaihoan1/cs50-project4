from factory import Factory
import factory
from network.models import User


class UserFactory(Factory):
    class Meta:
        model = User

    # bio = factory.Faker('lorem')

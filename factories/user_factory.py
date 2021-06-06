from factory import Factory
from network.models import User


class UserFactory(Factory):
    class Meta:
        model = User

    # bio = factory.Faker('lorem')

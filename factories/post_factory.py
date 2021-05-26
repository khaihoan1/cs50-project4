import factory
from faker import Faker
from post.models import Post
from .user_factory import UserFactory


faker = Faker()


class PostFactory(factory.Factory):
    class Meta:
        model = Post

    owner = factory.SubFactory(UserFactory)
    content = factory.Faker('text')
    created_time = factory.Faker('date_time')
    last_modified = factory.Faker('date_time')

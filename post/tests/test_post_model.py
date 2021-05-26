from datetime import datetime
from django.test import TestCase
from factories.post_factory import PostFactory
from network.models import User


class PostModelTestCase(TestCase):
    def test_create_new_post(self):
        new_post = PostFactory()

        self.assertEqual(type(new_post.content), str)
        self.assertEqual(type(new_post.created_time), datetime)
        self.assertEqual(type(new_post.last_modified), datetime)
        self.assertEqual(type(new_post.owner), User)

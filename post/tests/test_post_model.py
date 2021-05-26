from django.test import TestCase
from factories.post_factory import PostFactory
from network.models import User
from post.models import Post


class PostModelTestCase(TestCase):
    def test_create_new_post(self):
        new_post = PostFactory()

        self.assertIn('content', new_post)
        self.assertIn('created_time', new_post)
        self.assertIn('last_modified', new_post)
        self.assertEqual(type(new_post.owner), User)
    # def setUp(self):
    #     user = User.objects.create(email="hihi@hihi.com", password="asdasd", id=1)
    #     Post.objects.create(owner=user, content="asdsad", id=2)
    
    def test_hihi(self):
        # x = Post.objects.count()
        self.assertEqual(1, 1)

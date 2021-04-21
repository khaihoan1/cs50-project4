from django.db import models
from django.utils import timezone
from network.models import User
from post.models import Post
# Create your models here.


class Interact(models.Model):
    id = models.CharField(primary_key=True, null=False, max_length=20)
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interact):
    content = models.TextField()
    timestamp = models.TimeField()
    post_parent = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, db_column="post_parent")

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        return super(Comment, self).save(*args, **kwargs)


class Reply(Interact):
    content = models.TextField()
    timestamp = models.TimeField(auto_now=True)
    comment_parent = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, db_column="comment_parent")


class Like(Interact):
    id = models.AutoField(primary_key=True, null=False)
    is_like = models.BooleanField(null=False, default=True)
    post_parent = models.ForeignKey(Post, null=False, on_delete=models.CASCADE, db_column='post_parent')


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
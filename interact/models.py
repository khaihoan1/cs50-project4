from django.db import models
from django.utils import timezone
from network.models import User
from post.models import Post
# Create your models here.


class Interact(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interact):
    content = models.TextField()
    timestamp = models.TimeField()
    post_parent = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        db_column='post_parent',
        related_name='comments',
    )
    comment_ref = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name='children_comment'
    )

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        return super(Comment, self).save(*args, **kwargs)


# class Reply(Interact):
#     content = models.TextField()
#     timestamp = models.TimeField(auto_now=True)
#     comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, db_column="comment_parent")


class Like(Interact):
    is_like = models.BooleanField(null=False, default=True)
    post_parent = models.ForeignKey(
        Post,
        null=False,
        on_delete=models.CASCADE,
        db_column='post_parent',
        related_name='likes'
    )

    def get_count_to_update(self, is_like: bool):
        return Like.objects.filter(post_parent=self.post_parent, is_like=is_like).count()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'post_parent'], name='unique_like')
        ]


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follow')
        ]

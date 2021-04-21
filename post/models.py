from django.db import models
from network.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    id = models.CharField(primary_key=True, null=False, max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False, blank=False)
    count_like = models.IntegerField(default=0)
    created_time = models.DateTimeField()
    last_modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update last_modified '''
        if not self.id:
            count = Post.objects.count()
            self.id = "PO" + str(count)
            self.created_time = timezone.now()
        self.last_modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post:post_detail', kwargs={'pk': self.pk})

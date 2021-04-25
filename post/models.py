from django.db import models
from network.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False, blank=False)
    created_time = models.DateTimeField()
    last_modified = models.DateTimeField(auto_now=True)

    def save(self):
        if not self.pk:
            self.created_time = timezone.now()
        return super().save()

    def get_absolute_url(self):
        return reverse('post:post_detail', kwargs={'pk': self.pk})

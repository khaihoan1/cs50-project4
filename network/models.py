from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar_pic = models.ImageField(null=True, blank=True)

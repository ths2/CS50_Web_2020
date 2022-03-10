from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import Field


class User(AbstractUser):
    pass
    following = models.ManyToManyField('self', blank=True)
    followers = models.ManyToManyField('self', blank=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_user')
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes_users")
    deslikes = models.ManyToManyField(User, blank=True, related_name="dislikes_users")


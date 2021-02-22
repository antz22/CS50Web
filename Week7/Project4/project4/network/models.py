from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    datetime = models.DateTimeField()
    

class Profile(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(User, related_name="followers", blank=True)
    # a user / follower can have many follows, follow many people
    # -> other way, follows have many followers.


class Like(models.Model):
    # defined for each user, will have many posts in their "like" object
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    posts = models.ManyToManyField(Post, related_name="likes", blank=True)
    # make it default = 0?
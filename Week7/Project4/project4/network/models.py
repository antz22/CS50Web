from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    datetime = models.DateTimeField()
    # likes = models.ForeignKey(Like, on_delete=models.CASCADE, related_name="likes")

    def serialize(self):
        return {
            "user": self.user.username,
            "content": self.content,
            # "likes": Post.objects.get(id=self.id).likes.all().count(), # not sure about this one,
            # "likes": None,
            "datetime": self.datetime.strftime("%b %d %Y, %I:%M %p"),
        }

class Profile(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(User, related_name="followers", blank=True)
    # a user / follower can have many follows, follow many people
    # -> other way, follows have many followers.



class Like(models.Model):
    like = models.BooleanField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    # make it default = 0?
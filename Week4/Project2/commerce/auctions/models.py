from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    photo = models.TextField(blank=True, null=True) # optional field
    # category = models.ForeignKey(Category, related_name="category") 
    category = models.CharField(max_length=64, blank=True, null=True) 


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField()


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()


class Category(models.Model):
    category = models.ForeignKey(Listing, related_name="category")
    # this is not right...

class Watchlist(models.Model):
    # how to relate it to user? is many to many field correct? is it only on watchlist for just that user?
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist") # or instead of listing, users?

# many to many field vs foreign keys?

# figure out the stuff with foreign keys
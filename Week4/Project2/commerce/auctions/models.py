from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist")


class Category(models.Model):
    category = models.CharField(max_length=64, blank=True, null=True)
    # category = models.ForeignKey(Category, related_name="listings?") 
    # listings = models.ManyToManyField(Listing, related_name="listings") # cuz it has multiple?
    # listings = models.ForeignKey(Listing, related_name="listings")
    # this is not right...


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=9)
    photo = models.TextField(blank=True, null=True) # optional field
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listingsss", blank=True, null=True) 
    # category = models.CharField(max_length=64, blank=True, null=True) 


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(decimal_places=2, max_digits=9)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()



class Watchlist(models.Model):
    # how to relate it to user? is many to many field correct? is it only on watchlist for just that user?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist") # or instead of listing, users?

# many to many field vs foreign keys?

# figure out the stuff with foreign keys
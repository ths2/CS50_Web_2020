from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    image_url = models.CharField(max_length=500)
    start_bid = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.id}: {self.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
class Bid(models.Model):
    value_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    
    def __str__(self):
       return f"{self.id}: {self.value_bid}"

class Category(models.Model):
    name = models.CharField(max_length=40)
    listings = models.ManyToManyField(Listing, blank=True, related_name="categories")
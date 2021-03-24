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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
class Bid(models.Model):
    value_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
class Category(models.Model):
    name = models.CharField(max_length=40)
    listings = models.ManyToManyField(Listing, blank=True, related_name="categories")
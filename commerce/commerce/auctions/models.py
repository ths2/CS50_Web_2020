from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Listing(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image_url = models.CharField(max_length=300, blank=True)   
    initial_Price = models.FloatField()
    user_listing = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator" )
    watch_list_users = models.ManyToManyField(User, blank=True, related_name="users")

    def __str__(self):
        return f"{self.name} ({self.description})"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user" )
    value = models.FloatField()

    def __str__(self):
        return f"{self.listing} ({self.value})"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="k")
    comment = models.CharField(max_length = 350)


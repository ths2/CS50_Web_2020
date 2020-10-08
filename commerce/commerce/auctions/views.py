from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#Create Listing
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bind = request.POST["bind"]
        image = request.POST["image"]

        user = request.user

        listing = Listing(name=title, description=description, image_url=image, initial_Price=bind, user_listing=user)
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/userlisting.html")
    

# Listing Page 
def listing_page(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    users = listing.watch_list_users.all()

    if request.method == "POST":  
        add = request.POST["ar"] 
        user_id = request.POST["user_id"]

        user = User.objects.get(pk=user_id)
        listing.watch_list_users.add(user)
        
        users = listing.watch_list_users.all()


    return render(request, "auctions/listingpage.html", {
        "listing": listing,
        "users": users
    })

def watchlist(request):
    user_id = request.user.id
    listings = Listing.objects.filter(watch_list_users=user_id)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
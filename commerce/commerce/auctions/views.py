from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bid

def index(request):
    listing = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listing
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

        listing = Listing(name=title, description=description, image_url=image, initial_Price=bind, user_listing=user, 
            highest_bidder=user)
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/userlisting.html")
    

# Listing Page 
def listing_page(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    users = listing.watch_list_users.all()
    error_mensage = None

    if request.method == "POST":  
        action = request.POST["action"] 
        user_id = request.user.id 

        user = User.objects.get(pk=user_id)

        if action == "add":
            listing.watch_list_users.add(user)           
        elif action == "rem":
            listing.watch_list_users.remove(user)
        elif action == "bin":
            price = listing.initial_Price
            value = float(request.POST["value"])
            if value > price:
                listing.initial_Price = value
                listing.highest_bidder = user
                binds = Bid(listing_id=listing_id, user=user, value=value )
                binds.save()
                listing.save()
            else:
                error_mensage = f"Bid must be greater than {price}" 
        elif action == "can":
            listing.active_listing = False
            listing.save()
        elif action == "comment":
            comment = Comment(user=user, comment=request.POST["comment"])
            comment.save()
            listing.comments.add(comment)
            listing.save()
            print("oi")


    username = request.user.username
    user = users.filter(username=username)
    user_creator = listing.user_listing.username
    pertence = False
    highest_bidder = listing.highest_bidder.username
    all_comments = listing.comments.all()
    if username == user_creator:
        pertence = True

    if user:
        if not listing.active_listing:
            if username == highest_bidder:
                return render(request, "auctions/listingpage.html", {
                "listing": listing,
                "present_user": user,
                "error_mensage":error_mensage,
                "user_creator": pertence,
                "hisghest_bidder": highest_bidder,
                "comments": all_comments
            })
        return render(request, "auctions/listingpage.html", {
            "listing": listing,
            "present_user": user,
            "error_mensage":error_mensage,
            "user_creator": pertence,
            "comments": all_comments
        })

    return render(request, "auctions/listingpage.html", {
        "listing": listing,
         "user_creator": pertence,
         "error_mensage":error_mensage,
         "comments": all_comments
    })

def watchlist(request):
    user_id = request.user.id   
    listings = Listing.objects.filter(watch_list_users=user_id)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
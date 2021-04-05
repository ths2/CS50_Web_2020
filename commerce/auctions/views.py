from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Category
from .forms import NewListingForm

def index(request):
    listing = Listing.objects.get(id=1)
    categories = listing.categories.all()
    
    

    return render(request, "auctions/index.html", {
        "listing": listing,
        "categories": categories,   
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


def create_listing(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewListingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

            creator = request.user
            title = form.cleaned_data["listing_title"]
            description = form.cleaned_data["listing_discription"]
            image_url = form.cleaned_data["listing_image"]
            start_bid = form.cleaned_data["start_bid"]

            #Create a new listing
            l = Listing(title=title, description=description, 
                image_url=image_url, start_bid=start_bid, creator=creator)
            l.save()    

            #Defines the categories of the listings
            cat = form.cleaned_data["category"]
            
            for c in cat:
                category = Category.objects.get(pk=c)
                category.listings.add(l)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewListingForm()

    return render(request, 'auctions/create_listing.html', {'form': form})
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Category
from .forms import NewListingForm, BindListing

from django.db.models import Max

def index(request):
    listings = Listing.objects.all()
    list1 = []
    list2 = []
   
    # Search the list's max value 
    for l in listings:
        a = l.listing_bids.all().aggregate(Max('value_bid'))["value_bid__max"]
        list1 = [l, a]
        list2.append(list1)
    
   
    return render(request, "auctions/index.html", {
        "listings": list2
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

def listing_page(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    maxPrice = listing.listing_bids.all().aggregate(Max('value_bid'))["value_bid__max"]

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BindListing(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

            creator = request.user
            price = form.cleaned_data["price_bind"]

            '''# Add a new price for the listing
            l = Listing(title=title, description=description, 
                image_url=image_url, start_bid=start_bid, creator=creator)
            l.save()    '''

            if maxPrice > price:
                print("O valor tem que ser maior que: " + str(maxPrice))

            form = BindListing()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BindListing()

    return render(request, "auctions/listing_page.html",{
        "listing": listing,
        "price": maxPrice,
        "form": form
    })
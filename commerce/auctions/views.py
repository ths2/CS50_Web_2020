from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse



from .models import *
from .forms import *

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
            
            return HttpResponseRedirect(reverse("index"))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewListingForm()

    return render(request, 'auctions/create_listing.html', {'form': form})

def listing_page(request, listing_id):
    
    user = request.user
    
    listing = Listing.objects.get(pk=listing_id)
    listingUser = listing.creator

    maxPrice = listing.listing_bids.all().aggregate(Max('value_bid'))["value_bid__max"]
    
    errormsg = False

    comments = Comment.objects.all().filter(listing=listing)

    #Checks whether the listing is on watchlisting
    existsWl=listing.watchlist.filter(pk = user.pk).exists()
 
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BindListing(request.POST)
        formClose = IsUser(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

            price = form.cleaned_data["price_bind"]

            '''# Add a new price for the listing
            l = Listing(title=title, description=description, 
                image_url=image_url, start_bid=start_bid, creator=creator)
            l.save()    '''

            if maxPrice == None:
                maxPrice = listing.start_bid
                if maxPrice <= price:
                    b = Bid(value_bid=price, user=user, listing=listing)
                    b.save()
                else:
                    errormsg = "O valor tem que ser maior ou igual a: " + str(maxPrice)
            elif maxPrice >= price:
                errormsg = "O valor tem que ser maior que: " + str(maxPrice)
            elif price > maxPrice:
                b = Bid(value_bid=price, user=user, listing=listing)
                b.save()
                maxPrice = price
                print("lance efutado com sucesso!")
        
        elif formClose.is_valid():
            listing.active = False
            listing.save()

    # if a GET (or any other method) we'll create a blank form

    form = BindListing()
    formWL = WatchListing()
    formClose = IsUser()
    formComment = CommentListing()

    isUser = False
    if user == listingUser:
        isUser = True

    if maxPrice == None:
        maxPrice = listing.start_bid

    #Verifica se a lista está ativa
    respWin = False 
    if not listing.active:
        userWin = Bid.objects.get(listing=listing, value_bid=maxPrice).user
        print(userWin)
        if user == userWin:
            respWin = "Congratulations, you win the listing!"
        

    return render(request, "auctions/listing_page.html",{
        "listing": listing,
        "price": maxPrice,
        "form": form,
        "formWL": formWL,
        "formClose": formClose,
        "isuser": isUser,
        "errormsg": errormsg,
        "formComment": formComment,
        "comments": comments,
        "respWin": respWin,
        "existsWl": existsWl
    })

#def listing_close(request, listing_id):


def listing_wl(request, listing_id):
    
    user = request.user
    listing = Listing.objects.get(pk=listing_id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formWL = WatchListing(request.POST)

        if formWL.is_valid(): 

            # Checks whether the listing is on watchlisting
            if listing.watchlist.filter(pk = user.pk).exists():
                listing.watchlist.remove(user)
                print("lista removida")
            else: 
                listing.watchlist.add(user)
                print("lista add")
    
    print("Ola mdf")
    return HttpResponseRedirect(reverse("lpage", args=([str(listing_id)])))



def listing_comments(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    l = str(listing_id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        text_comment = CommentListing(request.POST)

        if text_comment.is_valid(): 

           t= text_comment.cleaned_data["comment"]
           c = Comment(user=user, text=t, listing=listing)
           c.save()
    
    print(listing_id)
    return HttpResponseRedirect("/listingpage/"+l)

def watch_list(request):
    user = request.user

    watchlist = user.watchlist.all()

    return render(request, "auctions/watchlist.html",{
        "listings": watchlist,
    
    })

def categories(request):
    
    categories = Category.objects.all()
    
    return render(request, "auctions/categories.html",{
        "categories":  categories 
    })

def category_list(request, category_id):
    
    cat = Category.objects.get(pk=category_id)
    
    listings = cat.listings.all()

    print(listings)

    return render(request, "auctions/category_list.html",{
        "listings":  listings, 
    })




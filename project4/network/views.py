from asyncio.windows_events import NULL
from typing import NewType
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator

from .models import *

NUMBER_POST_PAGE = 10

def index(request):
   return HttpResponseRedirect(reverse("all_posts"))


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def create_post(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            post = request.POST["text"]

            newPost = Post(user = user, text = post)
            newPost.save()

            return HttpResponseRedirect(reverse("all_posts"))
        else:
            return render(request, "network/index.html")
    else:
        return render(request, "network/login.html", {
            "message": "You need to be logged in"
        })
        

def all_posts(request):


    posts = Post.objects.all()[::-1]

    paginator = Paginator(posts, NUMBER_POST_PAGE) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/allposts.html",{
        "page_obj": page_obj
    })

def perfil(request, perfil):
    user = request.user
    p = User.objects.get(username=perfil)
    posts = Post.objects.all().filter(user=p)
    followers = p.followers.all().count()
    following = p.following.all().count()
    
    userFollowingPerfil = False
    isUser = False
    if user == p:
        isUser = True
    else:
        userFollowingPerfil = p.followers.all().filter(username=user).exists()
        

    
    return render(request, "network/perfil.html", {
        "perfil":p, "posts":posts[::-1], 
        "followers":followers, 
        "following": following,
        "isuser":isUser,
        "userFollowingPerfil":userFollowingPerfil
    })

@csrf_exempt
@login_required
def follow(request):

    
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    idUser = data.get("idUser")
    follower = User.objects.get(username=idUser)
    user = User.objects.get(username=request.user)
    following = user.followers.all().filter(username = idUser).exists()
    
    if following:
        user.followers.remove(follower)
        return JsonResponse({"message": "Unfollow"}, status=201)
    else:
         user.followers.add(follower)
         return JsonResponse({"message": "Follow"}, status=201)
    


@login_required
def following(request):
    
    user = User.objects.get(username = request.user)
    following = user.followers.all()
    posts = Post.objects.all().filter(user__in = following).order_by("create_at")[::-1]

    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html",{
        "page_obj": page_obj
    })
    
    
@csrf_exempt
@login_required
def edit_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    
    id_post = data["id"]
 
    try:
        db_post = Post.objects.get(pk=id_post)   
        
        #Check credentials
        if db_post.user == request.user:
            print("OK")
        else:
            return JsonResponse({
            "error": "Wrong User"
        }, status=400)

        db_post.text = data['editedPost']
        db_post.save()

    except Post.DoesNotExist: 
        return JsonResponse({
            "error": "Post not found"
        }, status=400)

    return JsonResponse({"message": "Post edited successfully.", "status": 201}, status=201)

@csrf_exempt
@login_required
def likes(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    
    id_post = data["id"]
    func = data["func"]
    
    l, d = 0, 0

    try:
        db_post = Post.objects.get(pk=id_post)   
        user = request.user
        
        
        # Cheks if the user has already liked the post
        if func == 'l':
            if db_post.likes.all().filter(id = user.id).exists():
                db_post.likes.remove(user)
                l, d = -1, 0
            elif  db_post.deslikes.all().filter(id = user.id).exists():
                db_post.deslikes.remove(user)
                db_post.likes.add(user)
                l, d = 1, -1
            else:
                # Add a like to the post  
                db_post.likes.add(user)
                l, d = 1, 0
            db_post.save()

        # Cheks if the user has already disliked the post
        elif func == 'd':
            if db_post.deslikes.all().filter(id = user.id).exists():
                db_post.deslikes.remove(user)
                l, d = 0, -1
            elif  db_post.likes.all().filter(id = user.id).exists():
                db_post.likes.remove(user)
                db_post.deslikes.add(user)
                l, d = -1, 1
            else:
                # Add a dislike to the post  
                db_post.deslikes.add(user)
                l, d = 0, 1
            db_post.save()



        print(db_post.likes)


    except Post.DoesNotExist: 
        return JsonResponse({
            "error": "Post not found"
        }, status=400)

    return JsonResponse({"message": "Post edited successfully.", "status": 201, 'l':l, 'd':d}, status=201)
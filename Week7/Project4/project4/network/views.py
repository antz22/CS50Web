import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile, Like


def index(request):
    # posts = Post.objects.all()
    return render(request, "network/index.html")


@login_required
def following(request):

    user = request.user
    person = Profile.objects.get(person=user)
    follows = person.follows.all()


    return render(request, "network/following.html")

    # posts = Post.objects.filter()
    # how do you filter this? some sort of list of objects, some for loop to collect all of it?
    # hm... maybe you do it all in javascript


def posts(request, type):

    # Filter posts based on type (all, following, etc)
    if type == "all":
        posts = Post.objects.all()
    elif type == "following":
        posts = Post.objects.filter(
            pass
            # TODO
            # https://www.quora.com/How-do-I-use-Django-filter-with-multiple-values-on-the-same-query-field
            # seems to be the problem solved here
        )

    # Return emails in reverse chronological order...
    posts = posts.order_by("-datetime").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def post(request, post_id):

    post = Post.objects.get(pk=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes += 1
        post.save()
        return HttpResponse(status=204)


@login_required
def newpost(request):
    if request.method == "POST":
        user = request.user
        content = request.POST["content"]
        d = datetime.datetime.now()
        Post.objects.create(user=user, content=content, datetime=d)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "network/newpost.html")


def profile(request, user_id):

    # if someone tried to follow this profile
    if request.method == "POST":
        
        # the follower
        user = request.user
        person = Profile.objects.get(id=user_id)
        person.followers.add(user)

        # what to return? a lot of this is in javascript
    
    # profile of the requested user
    prof = User.objects.get(id=user_id) 
    # tricky here - followers gets all the followers associated with that user
    followers = User.followers.all().count()
    # follows gets all the reverses of the followers, the ones that the USER followed
    follows = User.follows.all().count()
    # make sure you get this to be in reverse chronological order, most recent post first
    posts = User.posts.all()    

    return render(request, "network/profile.html", {
        "profile": prof,
        "followers": followers,
        "follows": follows,
        "posts": posts
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

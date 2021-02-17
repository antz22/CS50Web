import time
import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile, Like


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj
    })


@login_required
def following(request):

    user = request.user
    person = Profile.objects.get(id=user.id)
    # follows = person.follows.all()
    followss = person.follows.all().values_list('id', flat=True).order_by('id')
    follows = list(followss)
    # an OR - returns all objects with user that is any one of them in the array of follows
    posts = Post.objects.filter(
        user__in=follows
    )

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": posts,
        "page_obj": page_obj
    })

    # posts = Post.objects.filter()
    # how do you filter this? some sort of list of objects, some for loop to collect all of it?
    # hm... maybe you do it all in javascript


# API Stuff
def posts(request, kind):

    # Get start and end points
    # start = int(request.GET.get("start") or 0)
    # end = int(request.GET.get("end") or (start + 9))

    # edits -> delete kind, delete api requests, delete from urls // return JSONReponse

    # Filter posts based on type (all, following, etc)
    if kind == "all":
        posts = Post.objects.all()

    elif kind == "following":
        user = request.user
        person = Profile.objects.get(id=user.id)
        follows = person.follows.all()
        # follows = person.follows.values_list('id', flat=True).order_by('id')

        # an OR - returns all objects with user that is any one of them in the array of follows
        posts = Post.objects.filter(
            user__in=[follows]
        )

    # paginator = Paginator(posts, 10)
    # post_number = request.GET.get('page')
    # post_obj = paginator.get_page(post_number)

    # time.sleep(1)

    # Return emails in reverse chronological order...
    posts = posts.order_by("-datetime").all()
    posts = serializers.serialize(
        'json', posts)  # but this is excluding likes! :(
    return JsonResponse(posts, safe=False)
    # return render(request, 'index.html', {'post_object': post_obj})

# API Stuff


def post(request, post_id):

    post = Post.objects.get(pk=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes += 1
        post.save()
        return HttpResponse(status=204)

# API stuff


def profiles(request, user_id):

    profile = Post.objects.get(id=user_id)
    posts = Post.objects.filter(user=profile)

    posts = posts.order_by("-datetime").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


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

    user = request.user

    # if someone tried to follow this profile
    if request.method == "POST":

        if 'follow' in request.POST:
            person = User.objects.get(id=user_id)
            user = Profile.objects.get(id=user.id)
            person.followers.add(user)
            # the follower

        elif 'unfollow' in request.POST:
            person = User.objects.get(id=user_id)
            user = Profile.objects.get(id=user.id)
            person.followers.remove(user)

        # what to return? a lot of this is in javascript

    # profile of the requested user
    prof1 = User.objects.get(id=user_id)
    # tricky here - followers gets all the followers associated with that user
    followers = prof1.followers.all().count()
    # follows gets all the reverses of the followers, the ones that the USER followed
    prof2 = Profile.objects.get(id=user_id)
    follows = prof2.follows.all().count()
    # make sure you get this to be in reverse chronological order, most recent post first
    posts = prof1.posts.all()

    user_obj = Profile.objects.get(id=user.id)

    if user_obj.id != prof1.id:
        if prof1 in user_obj.follows.all():
            followstatus = True
        else:
            followstatus = False
        valid = True
    else:
        followstatus = False
        valid = False

    return render(request, "network/profile.html", {
        "profile": prof1,
        "user": user,
        "followers": followers,
        "follows": follows,
        "posts": posts,
        "followstatus": followstatus,
        "valid": valid
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

            # addition here for profile
            profile = Profile.objects.create(person=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# i was too stupid to realize this before, but - all posts and following are probably done without javascript.
# need to look into pagination for that

# implement edit post and like and unlike - these should be somewhat similar to mail. learn the javascript.

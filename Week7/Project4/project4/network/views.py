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
    posts = Post.objects.all().order_by('-datetime')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user

    if request.user.is_authenticated:
        likes = Like.objects.get(user=user)

        return render(request, "network/index.html", {
            "posts": posts,
            "page_obj": page_obj,
            "user": user,
            "likes": likes
        })

    else:
        return render(request, "network/index.html", {
            "posts": posts,
            "page_obj": page_obj,
            "user": user
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
    ).order_by('-datetime')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user

    if request.user.is_authenticated:
        likes = Like.objects.get(user=user)

        return render(request, "network/following.html", {
            "posts": posts,
            "page_obj": page_obj,
            "user": user,
            "likes": likes
        })

    else:
        return render(request, "network/following.html", {
            "posts": posts,
            "page_obj": page_obj,
            "user": user
        })        




def post(request, post_id):

    post = Post.objects.get(pk=post_id)

    user = request.user

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            
            like = Like.objects.get(user=user)

            if post in like.posts.all():
                post.likes.remove(like)
                like.posts.remove(post)
            else:
                post.likes.add(like)
                like.posts.add(post)

            like.save()


        if data.get("content") is not None:
            post.content = data["content"]    

        post.save()
        

        return HttpResponse(status=204)
    
    else:
        return HttpResponse(status=400)



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
    posts = prof1.posts.all().order_by('-datetime')

    user_obj = Profile.objects.get(id=user.id)

    posts = Post.objects.filter(user=prof1)

    if user_obj.id != prof1.id:
        if prof1 in user_obj.follows.all():
            followstatus = True
        else:
            followstatus = False
        valid = True
    else:
        followstatus = False
        valid = False

    if request.user.is_authenticated:
        likes = Like.objects.get(user=request.user)

        return render(request, "network/profile.html", {
            "profile": prof1,
            "followers": followers,
            "follows": follows,
            "posts": posts,
            "followstatus": followstatus,
            "valid": valid,
            "posts": posts,
            "likes": likes
        })

    else:
    
        return render(request, "network/profile.html", {
            "profile": prof1,
            "followers": followers,
            "follows": follows,
            "posts": posts,
            "followstatus": followstatus,
            "valid": valid,
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

            # addition here for profile
            profile = Profile.objects.create(person=user)
            # addition here for likes
            like = Like.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




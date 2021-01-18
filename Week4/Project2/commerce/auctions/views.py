from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment

class NewListing(forms.Form):
    title = forms.CharField(label="Listing Title")
    description = forms.TextField(label="Description")
    price = forms.IntegerField(label="Price")
    photo = models.TextField(label="Photo URL", blank=True, null=True)
    category = form.CharField(label="Category", blank=True, null=True)



def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def listings(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)    
    comments = listing.comments.all()


    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user.get_username()

            context = {
                "listing": listing,
                "comments": comments,
                "user": user
            }

            bid = round(float(request.POST["bid"]), 2)
            comment0 = request.POST["comment"]

            if bid:
                if bid > listing.price:
                    bids = listing.bids.all()
                    for b in bids:
                        if bid > b:
                            listing.price = bid
                            listing.bidder = user
                            listing.save()
                            listing = Listing.objects.get(pk=listing_id)
                            return render(request, "auctions/listings.html", {
                                "listing": listing,
                                "comments": comments,
                                "user": user
                            })

                    messages.error(request, 'Bid must be greater than existing bids.')
                    return render(request, "auctions/listings.html", context)

                else:
                    messages.error(request, 'Bid must be greater than existing bids.')
                    return render(request, "auctions/listings.html", context)

                # if the request is because they submitted a bid. but how do you tell? is there an error otherwise?
            
            elif comment0:
                comment = Comment.objects.create(comment=comment0)
                comments = listing.comments.all()

                return render(request, "auctions/listings.html", {
                    "listing": listing,
                    "comments": comments,
                    "user": user
                })

                # fi the request is because they submitted a comment
            
            else:
                return render(request, "auctions/listings.html", context)

        else:
            messages.error(request, 'You must be logged in.')
            return render(request, "auctions/listings.html", {
                "listing": listing,
                "comments": comments,
                "user": user           
            })
   
    return render(request, "auctions/listings.html", context)

@login_required
def watchlist(request, user):
    # TODO

def categories(request):
    # TODO

def create(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            user = request.user.get_username()
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            photo = form.cleaned_data["photo"]
            category = form.cleaned_data["category"]

            listing = Listing.objects.create(user=user, bidder=user, title=title, description=description, price=price, photo=photo, cateogry=category)

            return render(request, "auctions/index.html", {
                "listings": Listing.objects.all()
            })

        else:
            return render(request, "auctions/create.html" {
                "form": form
            })
    
    return render(request, "auctions/create.html" {
        "form": NewListing()
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



# start using reverse correctly
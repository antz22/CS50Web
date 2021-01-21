from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category, Watchlist

class NewListing(forms.Form):
    title = forms.CharField(label="Listing Title", widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': "form-control"}))
    price = forms.DecimalField(label="Price", decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control"}))
    photo = forms.CharField(label="Photo URL", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    category = forms.CharField(label="Category", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))

    # ISSUE - django.forms doesn't have TEXTFIELD! what to do then? how long are descriptions?
    # how to resolve it with other models.py?



def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def listings(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)    
    comments = listing.comments.all()
    # watchlist = User.watchlist.all()


    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            wl = Watchlist.objects.get(user=user)
            watchl = wl.listings.all()

            if listing in watchl:
                watchlist = True
            else:
                watchlist = False

            context = {
                "listing": listing,
                "comments": comments,
                "user": user,
                "watchlist": watchlist
            }

            if 'bid' in request.POST:
                bid = float(format(float(request.POST["bid"]), '.2f'))
                if bid > listing.price:
                    # bids = listing.bids.all()
                    # for b in bids:
                        # if bid > b:
                    listing.price = bid
                    listing.bidder = user
                    listing.save()
                    listing = Listing.objects.get(pk=listing_id)
                    return render(request, "auctions/listings.html", {
                        "listing": listing,
                        "comments": comments,
                        "user": user,
                        "watchlist": watchlist
                    })

                    # messages.error(request, 'Bid must be greater than existing bids.')
                    # return render(request, "auctions/listings.html", context)

                else:
                    messages.error(request, 'Bid must be greater than existing bids.')
                    return render(request, "auctions/listings.html", context)

                # if the request is because they submitted a bid. but how do you tell? is there an error otherwise?
            
            elif 'comment' in request.POST:
                comment0 = request.POST["comment"]
                comment = Comment.objects.create(comment=comment0)
                comments = listing.comments.all()

                return render(request, "auctions/listings.html", {
                    "listing": listing,
                    "comments": comments,
                    "user": user,
                    "watchlist": watchlist
                })

                # fi the request is because they submitted a comment
            
            elif 'watch' in request.POST:
                watch = request.POST["watch"]
                user = request.user
                watching = Watchlist.objects.get(user=user)

                if listing in watching.listings.all():
                    watching.listings.remove(listing)
                    watchlist = False
                else:
                    watching.listings.add(listing)
                    watchlist = True

                return render(request, "auctions/listings.html", {
                    "listing": listing,
                    "comments": comments,
                    "user": user,
                    "watchlist": watchlist
                })

            else:
                return render(request, "auctions/listings.html", context)

        else:
            messages.error(request, 'You must be logged in.')
            return render(request, "auctions/listings.html", {
                "listing": listing,
                "comments": comments,
                "user": None,
                "watchlist": None        
            })

    if request.user.is_authenticated:
        user = request.user
        wl = Watchlist.objects.get(user=user)
        watchlist = wl.listings.all()

        context = {
            "listing": listing,
            "comments": comments,
            "user": user,
            "watchlist": watchlist
        }
        return render(request, "auctions/listings.html", context)
    else:

        context = {
            "listing": listing,
            "comments": comments,
            "user": None,
            "watchlist": None
        }
        return render(request, "auctions/listings.html", context)

@login_required
def watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.get(user=user)
    listings = watchlist.listings.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


    # problems here


def categories(request):
    categories = Category.objects.all()

    # problems here - cateogry.objects.all()?

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoriesv(request, category_id):
    category = Category.objects.get(pk=category_id)

    listings = category.listingsss.all()

    return render(request, "auctions/categoriesv.html", {
        "category": category,
        "listings": listings
    })

    # problems here - category.listings.all()? 


def create(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = float(format(form.cleaned_data["price"], '.2f'))
            photo = form.cleaned_data["photo"]
            category = form.cleaned_data["category"]

            categories = Category.objects.all()
            for cate in categories:
                if category == cate.category:
                    listing = Listing.objects.create(user=user, bidder=user, title=title, description=description, price=price, photo=photo, category=cate)
                    return HttpResponseRedirect(reverse("index"))
           
            cat = Category.objects.create(category=category) # create new instance of category separate from listing           
            listing = Listing.objects.create(user=user, bidder=user, title=title, description=description, price=price, photo=photo, category=cat)
            
             # wait but how to define category in the listing object?


            # create new instance of category?
            # cat = Category.objects.create(category=category)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    
    return render(request, "auctions/create.html", {
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

            # addition here to create watchlist with every user
            watch = Watchlist.objects.create(user=user)

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
# read through all this, make it neat, and make comments.
# set up admin.py, get watchlist, write the css.

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comment
from .forms import PostListingForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(active = True),
        "bids": Bid.objects.all(),
        "header": "Active listings"
    })

def closeditems(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(active = False),
        "bids": Bid.objects.all(),
        "header": " Closed Listings."
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

@login_required
def post(request):
    
    if request.method == "POST":

        form = PostListingForm(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            begining_bid = request.POST['begining_bid']
            image = request.POST['image']
            category = request.POST['category']
            user = request.user
        
            list_Post = Listing.objects.create(title = title,
                                user = user,
                                description = description,
                                image = image,
                                begining_bid = begining_bid,
                                category = category)
                                
            list_Post.save()
        
            return HttpResponseRedirect(reverse("index"))

    
    return render(request, "auctions/post.html",{
        "listing_form": PostListingForm(),
            
    })

def listing(request, listing_id):

    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
                "message": "Please log in to veiw items."
            })

    list_filter = Listing.objects.filter(id = listing_id).first()
    bid_filter = Bid.objects.filter(listing = list_filter)
    comment = Comment.objects.filter(listing = list_filter)
    user = request.user
    watch_list = Watchlist.objects.filter(user = user, listing = list_filter)
    
    highest_bid = list_filter.begining_bid

    for bid in bid_filter:
        if bid.current_price > highest_bid:
            highest_bid = bid.current_price
        
    return render(request, "auctions/listing.html", {
        "listing": list_filter,
        "highest_bid": highest_bid,
        "min_bid": (highest_bid + 1),
        "comments": comment,
        "watchlist":watch_list

         
    })
    
def categories(request):
    list_array = []
    list_all = Listing.objects.all()
    
    for listing in list_all:
        if listing.category:
            if listing.category not in list_array:
                list_array.append(listing.category)
                
    return render(request, "auctions/categories.html", {
        "categories": list_array
    })
@login_required
def category_choices(request, category):
    list_all_filter = Listing.objects.all().filter(category = category)
    return render(request, "auctions/category_choices.html", {
        "listings": list_all_filter
    })


@login_required
def watchlist(request):
    user = request.user
    watchlist_filter = Watchlist.objects.filter(user = user)
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_filter,
    })

@login_required
def add_watchlist(request, listing_id):
    user = request.user
    list_filter = Listing.objects.filter(id = listing_id).first()
    watch = Watchlist.objects.filter(user = user, listing = list_filter)
    
    if watch:
        watching_it = Watchlist.objects.get(user = user, listing = list_filter)
        watching_it.watching = True
        watching_it.save()
    else:
        Watchlist.objects.create(user = user, listing = list_filter, watching = True)

    
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def remove_watchlist(request, listing_id):
    user = request.user
    list_filter = Listing.objects.filter(id = listing_id).first()
    watch = Watchlist.objects.filter(user = user, listing = list_filter)
    
    watch.watching = False
    watch.delete()

    return HttpResponseRedirect(reverse("watchlist")) 

@login_required
def close(request, listing_id):
    
    list_filter = Listing.objects.filter(id = listing_id).first()
    bid_filterC = Bid.objects.filter(listing = list_filter).first()

    if list_filter.user == request.user and bid_filterC is None:
        list_filter.active = False
        list_filter.save()
        
        return HttpResponseRedirect(reverse('index'))
    
    elif list_filter.user == request.user and not bid_filterC is None:
            list_filter.active = False
            list_filter.final_bider = bid_filterC.user
            list_filter.save()
        
            return HttpResponseRedirect(reverse('index'))
    
    

    
    
    
@login_required        
def comment(request, listing_id):
    list_filter = Listing.objects.filter(id = listing_id).first()
    comment = request.POST.get('comment')
    user = request.user
    if request.method == 'POST':
        
        if comment:
            comment_create = Comment.objects.create(user = user, textfield = comment, listing = list_filter)
            list_filter.comments.add(comment_create)
            comment_create.save()
            
            return HttpResponseRedirect(reverse('listing', args = [listing_id]))

        else: 
            return render(request, "auctions/error.html", {
                "error": "Please make a comment."
            })    



def delete_comment(request, listing_id):
    list_filter = Listing.objects.filter(id = listing_id).first()
    comment_filter = Comment.objects.filter(listing = list_filter).first()

    if request.method == 'POST':
        comment_filter.delete()
        return HttpResponseRedirect(reverse('listing', args = [listing_id]))


def bidding(request, listing_id):
    list_filter = Listing.objects.filter(id = listing_id).first()
    bid_filter = Bid.objects.filter(listing = list_filter)
    user = request.user
    highest_bid = list_filter.begining_bid

    for current_bid in bid_filter:
        if current_bid.current_price > highest_bid:
            highest_bid = current_bid.current_price
        
    if request.method == 'POST':
        user = request.user
        current_price = request.POST.get('bid_price')
        listing = Listing.objects.filter(id = listing_id).first()

        
        if  current_price:
            current_price= int(current_price)

        else:
            current_price = None


        if current_price is None:

            return render(request, "auctions/error.html", {
                "error": "Please make a bid."
            })

        else: 
            if int(current_price) < highest_bid:
                
                return HttpResponseRedirect(reverse('listing', args = [listing_id]))
            
            bid_make = Bid.objects.create(current_price = int(current_price), user = user, listing = listing)
            bid_make.save()
            
            bidsaved = Bid.objects.filter(listing = listing).exclude(current_price = current_price)
            bidsaved.delete()
            
            return HttpResponseRedirect(reverse('listing', args = [listing_id]))
        
        


    
       
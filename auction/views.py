from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from .utils import item_in_watchlist
from .forms import CreateListingForm
from .models import AuctionListing, Bid, Comment, WatchList

# Create your views here.
def home(request):
    listings = AuctionListing.objects.all()
    # print('listingssssss:', listings)
    context = {
        'listings': listings,
        'title': 'Active Auctions'
    }
    return render(request, 'auction/home.html', context)

@login_required
def create_listing(request):
    """
    View to create a new listing.

    If the request method is POST, validates the submitted form and
    creates a new listing if it is valid. Otherwise, renders a form for
    the user to fill out.

    :param request: The request object
    :return: A rendered template or a redirect
    """
    if request.method == 'POST':
        form = CreateListingForm(request.POST, request.FILES)
        # The request.POST dictionary contains the submitted form data.
        # The request.FILES dictionary contains any uploaded files.
        # The CreateListingForm is initialized with the submitted data
        # and files.
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.current_price = form.cleaned_data['starting_price']
            listing.start_date = timezone.now()  # Set the start date to now
            listing.save()
            messages.success(request, 'Your listing has been created successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = CreateListingForm()
    
    return render(request, 'auction/create_listing.html', {'form': form})

def listing_detail(request, pk):
    listing = AuctionListing.objects.get(pk=pk)
    if request.user.is_authenticated:
        watchlist = WatchList.objects.get(user=request.user)
        watch_list = watchlist.items.all()
    else:
        watch_list = []
        
    context = item_in_watchlist(listing, watch_list, pk)
    context.update({
        'listing': listing,
    })
    
    return render(request, 'auction/listing_detail.html', context)

def categories(request, category):
    print(category)
    listings = AuctionListing.objects.filter(category=category.upper()) 
    print(listings)
    return render(request, 'auction/home.html', {'listings': listings})

def place_bid(request, pk):
    
    listing = AuctionListing.objects.get(pk=pk)
    
    if request.method == 'POST':
        try:
            listing.place_bid(request.user, float(request.POST['bid_amount']))
            messages.success(request, 'Your bid has been placed successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, e)
            return redirect('listing_detail', pk=pk)
 
@login_required        
def watchlist(request):
    watchlist = WatchList.objects.get(user=request.user)
    watch_list = watchlist.items.all()
    
    context = {
        'listings': watch_list,
        'title': 'Watchlist',
    }
    return render(request, 'auction/home.html', context)

@login_required
def add_to_watchlist(request, pk):
    listing = AuctionListing.objects.get(pk=pk)
    listing.add_to_watchlist(request.user)
    
    watchlist = WatchList.objects.get(user=request.user)
    watchlist.items.add(listing)
    
    watchlist_items = WatchList.objects.filter(user=request.user)
    print(watchlist_items)

    watch_list = watchlist.items.all()
        
    context = item_in_watchlist(listing, watch_list, pk)

    return render(request, 'auction/snippets/watchlist_button.html', context)

@login_required
def remove_from_watchlist(request, pk):
    listing = AuctionListing.objects.get(pk=pk)
    # listing.remove_from_watchlist(request.user)
    WatchList.objects.get(user=request.user).items.remove(listing)
    watch_list = WatchList.objects.all()
    
    context = item_in_watchlist(listing, watch_list, pk)
    return render(request, 'auction/snippets/watchlist_button.html', context)


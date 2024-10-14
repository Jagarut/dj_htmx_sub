from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from .utils import item_in_watchlist
from .forms import CreateListingForm, CommentCreateForm
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
    commentform = CommentCreateForm()
    comments = listing.comments.all()
    
    if request.user.is_authenticated:
        # Get the user's watchlist. If the user does not have a watchlist, create one.
        # The [0] at the end of the line is needed because get_or_create returns a tuple
        # where the first element is the object and the second element is a boolean
        # indicating whether the object was created or not. We are only interested in the
        # object itself, so we use [0] to get the first element of the tuple.
        watchlist = WatchList.objects.get_or_create(user=request.user)[0]
        watch_list = watchlist.items.all()
    else:
        watch_list = []
        
    context = item_in_watchlist(listing, watch_list, pk)
    context.update({
        'listing': listing,
        'commentform': commentform,
        'comments': comments,
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
    watchlist = WatchList.objects.get_or_create(user=request.user)[0]
    watch_list = watchlist.items.all()
    
    if not watch_list:
        title = 'Tu lista de seguimiento está vacía'
    else:
        title = 'Watchlist'
        
    context = {
        'listings': watch_list,
        'title': title,
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

def search(request):
    query = request.GET.get('search', '')

    listings = AuctionListing.objects.filter(title__icontains=query)
    
    context = {
        'listings': listings,
        'title': 'Search Results'
    }
    if not listings:
        context['title'] = 'No results found'

    return render(request, 'auction/home.html', context)

@login_required
def add_comment(request, pk):
    listing = get_object_or_404(AuctionListing, pk=pk)
    print(listing)
    if request.method == 'POST':
        listing.add_comment(request.user, request.POST['text'])
        comment = Comment.objects.latest('created_at')
        return render(request, 'auction/snippets/comments.html', {'comment': comment})
    else:
        # Create an empty form
        commentform = CommentCreateForm()
    
    context = {
        'listing': listing,
        'commentform': commentform
    }
    
   
    return render(request, 'auction/listing_detail.html', context)

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
 
    if request.method == 'DELETE':
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully!')
        return HttpResponse('')
    else:
        messages.error(request, 'There was an error deleting your comment.')
        return HttpResponse('')
    

def edit_comment(request, comment_pk):
    pass
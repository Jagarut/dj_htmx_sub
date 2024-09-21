from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import CreateListingForm
from .models import AuctionListing

# Create your views here.
def home(request):
    listings = AuctionListing.objects.all()
    context = {'listings': listings}
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
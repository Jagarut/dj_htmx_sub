from .models import AuctionListing
def category_context(request):
    categories = [category[1] for category in AuctionListing.CATEGORY_CHOICES]
    # print(categories)
    return {'categories': categories}
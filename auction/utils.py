from django.urls import reverse
def item_in_watchlist(listing, watch_list, pk):
    if listing in watch_list:
        text_button = 'Remove from watchlist'
        color = 'gray'
        url = reverse('remove_from_watchlist', args=[pk])
    else:
        text_button = 'Add to watchlist'
        color = 'orange'
        url = reverse('add_to_watchlist', args=[pk])
        
    context = {
        # 'listing': listing,
        'text_button': text_button,
        'color': color,
        'url': url
    }
    return context

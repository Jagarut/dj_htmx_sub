from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inactive/", views.inactive, name="inactive_auctions"),
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<str:category>/', views.categories, name='categories'),
    path('bid/<int:pk>/', views.place_bid, name='place_bid'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add_to_watchlist/<int:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:pk>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('search/', views.search, name='search'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'), 
    path('edit_comment/<int:pk>/', views.edit_comment, name='edit_comment'), 
    path('close_bid/<int:pk>/', views.close_bid, name='close_bid'),  
    path('open_bid/<int:pk>/', views.open_bid, name='open_bid'),  
    # path('listing/<int:pk>/bid/', views.bid, name='bid'), 
    #  path('listing/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    #  path('listing/<int:pk>/bid/', views.bid, name='bid'),
    #  path('listing/<int:pk>/close/', views.close, name='close'),
    #  path('listing/<int:pk>/comment/', views.comment, name='comment'),
    #  path('listing/<int:pk>/comment/delete/<int:comment_pk>', views.delete_comment, name='delete_comment'),
]
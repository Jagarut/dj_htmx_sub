from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
     path('create/', views.create_listing, name='create_listing'),
     path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
     path('listing/<str:category>/', views.categories, name='categories'),
     path('bid/<int:pk>/', views.place_bid, name='place_bid'),
     path('watchlist/', views.watchlist, name='watchlist'),
     path('add_to_watchlist/<int:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
     path('remove_from_watchlist/<int:pk>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    #  path('listing/<int:pk>/bid/', views.bid, name='bid'),
    #  path('listing/<int:pk>/close/', views.close, name='close'),
    #  path('listing/<int:pk>/comment/', views.comment, name='comment'),
    #  path('listing/<int:pk>/comment/delete/<int:comment_pk>', views.delete_comment, name='delete_comment'),
]
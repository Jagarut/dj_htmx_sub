from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
     path('create/', views.create_listing, name='create_listing'),
     path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    #  path('listing/<int:pk>/bid/', views.bid, name='bid'),
    #  path('listing/<int:pk>/close/', views.close, name='close'),
    #  path('listing/<int:pk>/comment/', views.comment, name='comment'),
    #  path('listing/<int:pk>/watchlist/', views.watchlist, name='watchlist'),
    #  path('listing/<int:pk>/comment/delete/<int:comment_pk>', views.delete_comment, name='delete_comment'),
]
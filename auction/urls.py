from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
     path('create/', views.create_listing, name='create_listing'),
]
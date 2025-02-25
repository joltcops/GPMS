from django.contrib import admin
from django.urls import path, include  # Import include
from . import views

urlpatterns = [
    path("citizens/<str:fields>/", views.get_citizens),
    path('addcitizen/', views.addcitizen),
]

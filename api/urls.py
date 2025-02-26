from django.contrib import admin
from django.urls import path, include  # Import include
from . import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('add-citizen/', views.add_citizen, name = 'add_citizen'),
    path("citizens/<str:fields>/", views.get_citizens),
    path("citizens/", views.getcitizens),
    path('addcitizen/', views.addcitizen),
    path('citizenslist/', views.citizen_list, name='citizen_list'),
    path('citizenlist/<str:citizen_id>/', views.citizen_detail, name='citizen_detail'),
    path('schemes/', views.getschemes),
]

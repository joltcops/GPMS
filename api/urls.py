from django.contrib import admin
from django.urls import path, include  # Import include
from . import views
from .views import empcitdetails, CitizenUpdateView, HouseholdUpdateView, LandUpdateView,UserUpdateView, AssetUpdateView

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('add-citizen/', views.add_citizen, name = 'add_citizen'),
    path('citizenslist/', views.citizen_list, name='citizen_list'),
    path('citizenlist/<str:citizen_id>/', views.citizen_detail, name='citizen_detail'),
    path('empcitdetails/<str:citizen_id>/', views.empcitdetails, name='emp_citizen_detail'),
    path('citihome/<str:citizen_id>/', views.cithome, name='citizen_home'),
    path('mycertificate/<str:citizen_id>/', views.mycertificate, name='my_certificates'),
    path('mybenefits/<str:citizen_id>/', views.mybenefits, name='my_benefits'),
    path('mytax/<str:citizen_id>/', views.mytax, name='my_tax'),
    path('applycertificate/<str:citizen_id>/', views.applycertificate, name='apply_certificate'),
    path('applybenefits/<str:citizen_id>/', views.applybenefits, name='apply_benefits'),
    path('logout/', views.logout, name='logout'),
    path('emphome/<str:emp_id>/', views.emphome, name='emp_home'),
    path('empdetails/<str:emp_id>/', views.empdetail, name='emp_detail'),
    path('citizen/edit/<str:pk>/', CitizenUpdateView.as_view(), name='citizen_edit'),
    path('household/edit/<str:pk>/', HouseholdUpdateView.as_view(), name='household_edit'),
    path('land/edit/<str:pk>/', LandUpdateView.as_view(), name='land_edit'),
    path('addland/<str:citizen_id>/', views.add_land, name='add_land'),
    path('addassets/',views.add_assets,name='add_assets'),
    path('user/edit/<str:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('addvaccine/<str:citizen_id>/', views.add_vaccine, name='add_vaccine'),
    path('assets_list/', views.assetslist, name='assetslist'),
    path('delete-land/<str:land_id>/', views.delete_land, name='delete_land'),
    path('delete-vaccine/<str:vaccination_id>/', views.delete_vaccine, name='delete_vaccine'),
    path('delete-citizen/<str:citizen_id>/', views.delete_citizen, name='delete_citizen'),
    path('delete-asset/<str:asset_id>/', views.delete_asset, name='delete_asset'),
    path('asset/edit/<str:pk>/', AssetUpdateView.as_view(), name='asset_edit'),

]

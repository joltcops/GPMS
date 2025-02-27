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
    path('login_page/', views.login_page, name = 'login_page'),
    path('panchayat_details/', views.panchayat_details, name = 'panchayat_details'),
    path('environment_data/', views.environment_data, name = 'environment_data'),
    path('agriculture_data/', views.agriculture_data, name = 'agriculture_data'),
    path('infrastructure_data/', views.infrastructure_data, name = 'infrastructure_data'),
    path('infrastructure_data_login/', views.infrastructure_data_login, name = 'infrastructure_data_login'),
    path('environment_data_login/', views.environment_data_login, name = 'environment_data_login'),
    path('agriculture_data_login/', views.agriculture_data_login, name = 'agriculture_data_login'),
    path('census_data_login/', views.census_data_login, name = 'census_data_login'),
    path('government_monitor/', views.government_monitor, name = 'government_monitor'),
    path('census_data/', views.census_data_func, name = 'census_data'),
    path('login_view/', views.login_view, name = 'login_view'),
    path('infrastructure_data_monitor/', views.infrastructure_data_monitor, name = 'infrastructure_data_monitor'),
    path('env_data_monitor/', views.env_data_monitor, name = 'env_data_monitor'),
    path('members/<str:household_id>', views.members, name = 'members'),
    path('certificates/<str:citizen_id>', views.certificates, name = 'certificates'),
    path('apply_certificate/', views.apply_certificate, name = 'apply_certificate')
]

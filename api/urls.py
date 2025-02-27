from django.contrib import admin
from django.urls import path, include  # Import include
from . import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('add-citizen/', views.add_citizen, name = 'add_citizen'),
    path("citizens/<str:fields>/", views.get_citizens),
    path("citizens/", views.getcitizens),
    path('addcitizen/', views.addcitizen),
    path('apply_benefit/', views.add_benefit_application, name = 'apply_benefit'),
    path('approve_certificate/', views.approve_certificate, name = 'approve_certificate'),
    path('citizenslist/', views.citizen_list, name='citizen_list'),
    path('citizenlist/<str:citizen_id>/', views.citizen_detail, name='citizen_detail'),
    path('schemes/', views.getschemes, name = 'schemes'),
    path('panchayat_details/',views.panchayat_details,name='panchayat_details'),
    path('environment_data/',views.environment_data,name='environment_data'),
    path('infrastructure_data/',views.infrastructure_data,name='infrastructure_data'),
    path('agriculture_data/',views.agriculture_data,name='agriculture_data'),
    path('login_page/',views.login_page,name='login_page'),
    path('approve_certificate/<int:application_id>/<int:employee_id>/', views.approve_certificate, name='approve_certificate'),
]

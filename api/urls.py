from django.contrib import admin
from django.urls import path, include  # Import include
from . import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('add-citizen/', views.add_citizen, name = 'add_citizen'),
    path('citizenslist/', views.citizen_list, name='citizen_list'),
    path('citizenlist/<str:citizen_id>/', views.citizen_detail, name='citizen_detail'),
    path('citihome/<str:citizen_id>/', views.cithome, name='citizen_home'),
    path('mycertificate/<str:citizen_id>/', views.mycertificate, name='my_certificates'),
    path('mybenefits/<str:citizen_id>/', views.mybenefits, name='my_benefits'),
    path('mytax/<str:citizen_id>/', views.mytax, name='my_tax'),
    path('applycertificate/<str:citizen_id>/', views.applycertificate, name='apply_certificate'),
    path('applybenefits/<str:citizen_id>/', views.applybenefits, name='apply_benefits'),
    path('logout/', views.logout, name='logout'),
    path('emphome/<str:emp_id>/', views.emphome, name='emp_home'),
    path('empdetails/<str:emp_id>/', views.empdetail, name='emp_detail'),
]

from django.contrib import admin
from django.urls import path, include  # Import include
from . import views
from .views import empcitdetails, CitizenUpdateView, HouseholdUpdateView, LandUpdateView,UserUpdateView, AssetUpdateView,SchemeUpdateView,CenUpdateView, HouseUpdateView, EnvUpdateView, EmployeeUpdateView, EmpUserUpdateView, EmpCitUpdateView

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('add-citizen/', views.add_citizen, name = 'add_citizen'),
    path('add-employee/', views.add_employee, name = 'add_employee'),
    path('citizenslist/', views.citizen_list, name='citizen_list'),
    path('employeeslist/', views.employee_list, name='employee_list'),
    path('citizenlist/<str:citizen_id>/', views.citizen_detail, name='citizen_detail'),
    path('empcitdetails/<str:citizen_id>/', views.empcitdetails, name='emp_citizen_detail'),
    path('admempdetails/<str:employee_id>/', views.admempdetails, name='adm_employee_detail'),
    path('admempdetails/<str:employee_id>/', views.admempdetails, name='adm_employee_detail'),
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
    path('employee/edit/<str:pk>/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('empuser/edit/<str:pk>/', EmpUserUpdateView.as_view(), name='empuser_edit'),
    path('empcit/edit/<str:pk>/', EmpCitUpdateView.as_view(), name='empcit_edit'),
    path('household/edit/<str:pk>/', HouseholdUpdateView.as_view(), name='household_edit'),
    path('land/edit/<str:pk>/', LandUpdateView.as_view(), name='land_edit'),
    path('env/edit/<str:pk>/', views.EnvUpdateView.as_view(), name='env_edit'),
    path('house/edit/<str:pk>/', views.HouseUpdateView.as_view(), name='house_edit'),
    path('addland/<str:citizen_id>/', views.add_land, name='add_land'),
    path('addassets/',views.add_assets,name='add_assets'),
    path('addtax/<str:citizen_id>/',views.add_tax,name='add_tax'),
    path('addenv/',views.add_env,name='add_env'),
    path('addhouse/',views.add_house,name='add_house'),
    path('addwelfareschemes/',views.add_welfare_schemes,name='add_welfare_schemes'),
    path('user/edit/<str:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('addvaccine/<str:citizen_id>/', views.add_vaccine, name='add_vaccine'),
    path('assets_list/', views.assetslist, name='assetslist'),
    path('houselist/', views.house_list, name='house_list'),
    path('envlist/', views.env_list, name='env_list'),
    path('delete-land/<str:land_id>/', views.delete_land, name='delete_land'),
    path('delete-vaccine/<str:vaccination_id>/', views.delete_vaccine, name='delete_vaccine'),
    path('delete-citizen/<str:citizen_id>/', views.delete_citizen, name='delete_citizen'),
    path('delete-employee/<str:employee_id>/', views.delete_employee, name='delete_employee'),
    path('delete-asset/<str:asset_id>/', views.delete_asset, name='delete_asset'),
    path('delete-scheme/<str:scheme_id>/', views.delete_scheme, name='delete_scheme'),
    path('delete-cen/<str:cen_id>/', views.delete_cen, name='delete_cen'),
    path('asset/edit/<str:pk>/', AssetUpdateView.as_view(), name='asset_edit'),
    path('env/edit/<str:pk>/', EnvUpdateView.as_view(), name='env_edit'),
    path('house/edit/<str:pk>/', HouseUpdateView.as_view(), name='house_edit'),
    path('scheme/edit/<str:pk>/', SchemeUpdateView.as_view(), name='scheme_edit'),
    path('cen/edit/<str:pk>/', CenUpdateView.as_view(), name='cen_edit'),
    path('census_data_list/', views.census_data_list, name='census_data_list'),
    path('welfare_schemes/', views.welfare_schemes_list, name='welfare_schemes_list'),
    path('addcensusdata/', views.add_census_data, name='add_census_data'),
    path('certificate_list/', views.view_cert_list, name='certificate_list'),
    path('benefit_list/', views.view_bene_list, name='benefits_list'),
    path('certificate_approve/<str:application_id>/', views.certificate_approve, name='certificate_approve'),
    path('benefit_approve/<str:application_id>/', views.benefit_approve, name='benefit_approve'),
    path('admhome/', views.admhome, name='adm_home'),
]

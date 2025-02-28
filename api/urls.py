from django.contrib import admin
from django.urls import path, include  # Import include
from . import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('add-citizen/', views.add_citizen, name = 'add_citizen'),
    path("citizens/<str:fields>/", views.get_citizens),
    path("citizens/", views.getcitizens),
    path('addcitizen/', views.addcitizen),
    path('apply_benefit/', views.add_benefit_application, name = 'apply_benefit'),
    path('approve_certificate/', views.approve_certificate, name = 'approve_certificate'),
    path('citizenslist/', views.citizen_list, name='citizen_list'),
    path('citizenlist/<str:citizen_id>/', views.citizen_detail, name='citizen_detail'),
    path('schemes/', views.getschemes, name = 'schemes'),
    path('schemes_gen/', views.getschemes_gen, name = 'schemes_gen'),
    path('show_date_scheme/', views.show_date_scheme, name = 'show_date_scheme'),
    path('show_stat_scheme/', views.show_stat_scheme, name = 'show_stat_scheme'),
    path('panchayat_details/',views.panchayat_details,name='panchayat_details'),
    path('environment_data/',views.environment_data,name='environment_data'),
    path('infrastructure_data/',views.infrastructure_data,name='infrastructure_data'),
    path('agriculture_data/',views.agriculture_data,name='agriculture_data'),
    path('show_income_agri/', views.show_income_agri, name = 'show_income_agri'),
    path('show_edu_agri/', views.show_edu_agri, name = 'show_edu_agri'),
    path('show_area_agri/', views.show_area_agri, name = 'show_area_agri'),
    path('login_page/',views.login_page,name='login_page'),
    path('approve_certificate/<int:application_id>/<int:employee_id>/', views.approve_certificate, name='approve_certificate'),
    path('general_env/', views.show_general_env, name = 'general_env'),
    path('general_env_1/', views.show_general_env_1, name = 'general_env_1'),
    path('show_date_env/', views.show_date_env, name = 'show_date_env'),
    path('show_val_env/', views.show_val_env, name = 'show_val_env'),
    path('show_above_avg_env/', views.show_above_avg_env, name = 'show_above_avg_env'),
    path('show_date_infra/', views.show_date_infra, name = 'show_date_infra'),
    path('show_loc_infra/', views.show_loc_infra, name = 'show_loc_infra'),
    path('infrastructure_data_login/', views.infrastructure_data_login, name = 'infrastructure_data_login'),
    path('environment_data_login/', views.environment_data_login, name = 'environment_data_login'),
    path('agriculture_data_login/', views.agriculture_data_login, name = 'agriculture_data_login'),
    path('census_data_login/', views.census_data_login, name = 'census_data_login'),
    path('government_monitor/', views.government_monitor, name = 'government_monitor'),
    path('census_data/', views.census_data_func, name = 'census_data'),
    path('show_general_census/', views.show_general_census, name = 'show_general_census'),
    path('census_date_count/', views.census_date_count, name = 'census_date_count'),
    path('census_pop_count/', views.census_pop_count, name = 'census_pop_count'),
    path('census_edu_count/', views.census_edu_count, name = 'census_edu_count'),
    path('census_vacc_count/', views.census_vacc_count, name = 'census_vacc_count'),
    path('census_income_count/', views.census_income_count, name = 'census_income_count'),
    path('login_view/', views.login_view, name = 'login_view'),
    path('infrastructure_data_monitor/', views.infrastructure_data_monitor, name = 'infrastructure_data_monitor'),
    path('env_data_monitor/', views.env_data_monitor, name = 'env_data_monitor'),
    path('members/<str:household_id>', views.members, name = 'members'),
    path('certificates/<str:citizen_id>', views.certificates, name = 'certificates'),
    path('apply_certificate/', views.apply_certificate, name = 'apply_certificate'),
    path('login_view_1/', views.login_view_1, name = 'login_view_1'),
    path('infra_gen/', views.infra_gen, name = 'infra_gen')
]

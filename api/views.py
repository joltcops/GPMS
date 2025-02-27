from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import citizenSerializer
from .models import citizen, household, panchayat_employees, users, land_records, scheme_enrollments, welfare_schemes, assets, vaccinations, certificate, tax
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection
from .forms import CitizenForm, LandForm, VaccineForm, AssetsForm
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import connection
from django.http import HttpResponseRedirect

def add_citizen(request):
    if request.method == 'POST':
        form = CitizenForm(request.POST)
        if form.is_valid():
            household_id = form.cleaned_data['household']
            parent_id = form.cleaned_data['parent']
            citizen_id=form.cleaned_data['citizen_id']
            name=form.cleaned_data['name']
            gender=form.cleaned_data['gender']
            dob=form.cleaned_data['dob']
            educational_qualification=form.cleaned_data['educational_qualification']
            income=form.cleaned_data['income']

            user_id=form.cleaned_data['citizen_id']
            role="CITIZEN"
            password_user='123456'

            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (user_id, role, password_user) VALUES (%s, %s, %s)", [user_id, role, password_user])
            cursor.execute("INSERT INTO citizen (citizen_id, name, gender, dob, educational_qualification, household_id, parent_id, income) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [citizen_id, name, gender, dob, educational_qualification, household_id, parent_id, income])
            
            print("Form is valid")
            print(form.cleaned_data)

            form = CitizenForm()
    else:
        form = CitizenForm()
    return render(request, 'employee/addcitizen.html', {'form': form})

def home_page(request):
    return render(request, 'index.html')

def citizen_list(request):
    citizens = citizen.objects.raw('SELECT * FROM citizen')
    return render(request, 'employee/citizen_list.html', {'citizens': citizens})

def citizen_detail(request, citizen_id):
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    return render(request, 'citizen/citizen_detail.html', {'citizen': citi})

def cithome(request, citizen_id):
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    return render(request, 'citizen/citizenhome.html', {'citizen': citi})

def mycertificate(request, citizen_id):
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM certificate WHERE applicant_id = %s', [citizen_id])
        certs = cursor.fetchall()
    return render(request, 'citizen/certificate.html', {'citizen': citi, 'certificates': certs})

def mybenefits(request, citizen_id):
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    schemes = scheme_enrollments.objects.raw('SELECT * FROM scheme_enrollments WHERE citizen_id = %s', [citizen_id])
    return render(request, 'citizen/benefits.html', {'citizen': citi, 'schemes': schemes})

def mytax(request, citizen_id):
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM tax WHERE payer_id = %s', [citizen_id])
        taxes = cursor.fetchall()
    return render(request, 'citizen/tax.html', {'citizen': citi, 'taxes': taxes})

def applycertificate(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/apply_cert.html', {'citizen': citi})

def applybenefits(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/apply_bene.html', {'citizen': citi})

def logout(request):
    return render(request, 'logout.html')

def emphome(request, emp_id):
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees WHERE employee_id = %s', [emp_id])[0]
    return render(request, 'employee/emphome.html', {'emp': emp})

def empdetail(request, emp_id):
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees WHERE employee_id = %s', [emp_id])[0]
    cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [emp.citizen_id.citizen_id])[0]
    print(emp.employee_id)
    return render(request, 'employee/empdetail.html', {'emp': emp, 'cit': cit})

def empcitdetails(request, citizen_id):
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    house = household.objects.raw('SELECT * FROM household join citizen using (household_id) WHERE citizen_id = %s', [citizen_id])[0]
    land = land_records.objects.raw('SELECT * FROM land_records WHERE citizen_id = %s', [citizen_id])
    senroll = scheme_enrollments.objects.raw('SELECT * FROM scheme_enrollments WHERE citizen_id = %s', [citizen_id])
    vac = vaccinations.objects.raw('SELECT * FROM vaccinations WHERE citizen_id = %s', [citizen_id])
    user = users.objects.raw('SELECT * FROM users join citizen ON users.user_id = citizen.citizen_id WHERE citizen.citizen_id = %s', [citizen_id])[0]
    members = citizen.objects.raw('SELECT * FROM citizen WHERE household_id = (SELECT household_id from citizen where citizen_id = %s)', [citizen_id])
    return render(request, 'employee/empcitdetails.html', {'citizen': citi, 'household': house, 'land': land, 'senroll': senroll, 'vaccinations': vac, 'user': user, 'members': members})

class CitizenUpdateView(UpdateView):
    model = citizen
    fields = ['name', 'gender', 'dob', 'educational_qualification', 'household_id', 'parent_id', 'income']
    template_name = 'api/generic_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        citizen_id = self.kwargs['pk']
        household_id = data['household_id'].household_id if data['household_id'] else None
        parent_id = data['parent_id'].citizen_id if data['parent_id'] else None
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE citizen
                SET name = %s, gender = %s, dob = %s, 
                    educational_qualification = %s, household_id = %s, 
                    parent_id = %s, income = %s
                WHERE citizen_id = %s
            ''', [data['name'], data['gender'], data['dob'], data['educational_qualification'],
                  household_id, parent_id, data['income'], citizen_id])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.kwargs['pk']})

class HouseholdUpdateView(UpdateView):
    model = household
    fields = ['address', 'category', 'income']
    template_name = 'api/generic_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        household_id = self.kwargs['pk'] 
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE household
                SET address = %s, category = %s, income = %s
                WHERE household_id = %s
            ''', [data['address'], data['category'], data['income'], household_id])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.object.household_id})


class LandUpdateView(UpdateView):
    model = land_records
    fields = ['area_acres', 'crop_type']
    template_name = 'api/generic_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        land_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE land_records
                SET area_acres = %s, crop_type = %s
                WHERE land_id = %s
            ''', [data['area_acres'], data['crop_type'], land_id])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.object.land_id})

    
class UserUpdateView(UpdateView):
    model = users
    fields = ['role', 'password_user']
    template_name = 'api/generic_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        user_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE users
                SET role = %s, password_user = %s
                WHERE user_id = %s
            ''', [data['role'], data['password_user'], user_id])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.object.user_id})

    
def add_land(request, citizen_id):
    if request.method == 'POST':
        form = LandForm(request.POST)
        if form.is_valid():
            land_id = form.cleaned_data['land_id']
            area_acres = form.cleaned_data['area_acres']
            crop_type = form.cleaned_data['crop_type']
            cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
            print("Form is valid")
            print(form.cleaned_data)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO land_records (land_id, citizen_id, area_acres, crop_type) VALUES (%s, %s, %s, %s)", [land_id, cit.citizen_id, area_acres, crop_type])
            form = LandForm()
    else:
        form = LandForm()
    return render(request, 'employee/addland.html', {'form': form})

def add_vaccine(request, citizen_id):
    if request.method == 'POST':
        form = VaccineForm(request.POST)
        if form.is_valid():
            vacc_id = form.cleaned_data['vaccination_id']
            vacc_type = form.cleaned_data['vaccine_type']
            data_ad = form.cleaned_data['date_administered']
            cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
            print("Form is valid")
            print(form.cleaned_data)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO vaccinations (vaccination_id, citizen_id, vaccine_type, date_administered) VALUES (%s, %s, %s, %s)", [vacc_id, cit.citizen_id, vacc_type, data_ad])
            form = VaccineForm()
    else:
        form = VaccineForm()
    return render(request, 'employee/addvaccine.html', {'form': form})

@require_POST
def delete_land(request, land_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM land_records WHERE land_id = %s", [land_id])
        return JsonResponse({'status': 'success'})
    except land_records.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Land record not found'}, status=404)
    
@require_POST
def delete_vaccine(request, vaccination_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM vaccinations WHERE vaccination_id = %s", [vaccination_id])
        return JsonResponse({'status': 'success'})
    except vaccinations.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vaccine record not found'}, status=404)
    
@require_POST
def delete_citizen(request, citizen_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", [citizen_id])
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def assetslist(request):
    asset = assets.objects.raw('SELECT * FROM assets')
    return render(request, 'employee/assets_list.html', {'assets': asset})
    
def add_assets(request, citizen_id):
    if request.method == 'POST':
        form = AssetsForm(request.POST)
        if form.is_valid():
            asset_id = form.cleaned_data['asset_id']
            type = form.cleaned_data['type']
            location = form.cleaned_data['location']
            installation_date = form.cleaned_data['installation_date']
            budget = form.cleaned_data['budget']
            print("Form is valid")
            print(form.cleaned_data)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO assets (asset_id, type, location, installation_date, budget) VALUES (%s, %s, %s, %s, %s)", [asset_id, type, location, installation_date, budget])
            form = AssetsForm()
    else:
        form = AssetsForm()
    return render(request, 'employee/addassets.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import citizenSerializer
from .models import citizen, household, panchayat_employees, users, land_records, scheme_enrollments, welfare_schemes, assets, vaccinations
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection
from .forms import CitizenForm, LandForm, VaccineForm
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.views.decorators.http import require_POST

# @api_view(["GET"])
# def get_citizens(request, fields):
#     allowed_fields = {"name", "educational_qualification", "age", "gender"}  # Allowed columns
#     requested_fields = fields.split(",")  # Convert comma-separated string to a list
#     invalid_fields = set(requested_fields) - allowed_fields  # Check for invalid fields

#     if invalid_fields:
#         return Response({"error": f"Invalid fields: {', '.join(invalid_fields)}"}, status=400)

#     fields_query = ", ".join(requested_fields)  # Convert list back to SQL-safe string

#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT {fields_query} FROM citizen")  # Query only required fields
#         results = cursor.fetchall()

#     data = [dict(zip(requested_fields, row)) for row in results]  # Convert result to JSON format
#     return Response(data)  # DRF handles the response

def add_citizen(request):
    if request.method == 'POST':
        form = CitizenForm(request.POST)
        if form.is_valid():
            household_id = form.cleaned_data['household']
            parent_id = form.cleaned_data['parent']
            household_inst = household.objects.get(household_id=household_id)
            parent_inst = citizen.objects.get(citizen_id=parent_id)
            citi = citizen(
                citizen_id=form.cleaned_data['citizen_id'],
                name=form.cleaned_data['name'],
                gender=form.cleaned_data['gender'],
                dob=form.cleaned_data['dob'],
                educational_qualification=form.cleaned_data['educational_qualification'],
                household=household_inst,
                parent=parent_inst,
                income=form.cleaned_data['income'],
            )
            user = users(
                user_id=form.cleaned_data['citizen_id'],
                role=3,
                password_user='123456',
            )
            print("Form is valid")
            print(form.cleaned_data)
            user.save()
            citi.save()
            form = CitizenForm()
    else:
        form = CitizenForm()
    return render(request, 'employee/addcitizen.html', {'form': form})

def home_page(request):
    return render(request, 'index.html')

def citizen_list(request):
    citizens = citizen.objects.all()
    return render(request, 'employee/citizen_list.html', {'citizens': citizens})

def citizen_detail(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/citizen_detail.html', {'citizen': citi})

def cithome(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/citizenhome.html', {'citizen': citi})

def mycertificate(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/certificate.html', {'citizen': citi})

def mybenefits(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/benefits.html', {'citizen': citi})

def mytax(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/tax.html', {'citizen': citi})

def applycertificate(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/apply_cert.html', {'citizen': citi})

def applybenefits(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen/apply_bene.html', {'citizen': citi})

def logout(request):
    return render(request, 'logout.html')

def emphome(request, emp_id):
    emp = get_object_or_404(panchayat_employees, employee_id=emp_id)
    return render(request, 'employee/emphome.html', {'emp': emp})

def empdetail(request, emp_id):
    emp = get_object_or_404(panchayat_employees, employee_id=emp_id)
    print(emp.employee_id)
    return render(request, 'employee/empdetail.html', {'emp': emp, 'cit': emp.citizen_id})

def empcitdetails(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    household = citi.household
    land = land_records.objects.filter(citizen_id=citi.citizen_id)
    senroll = scheme_enrollments.objects.filter(citizen_id=citi.citizen_id)
    vac = vaccinations.objects.filter(citizen_id=citi.citizen_id)
    user = users.objects.get(user_id=citi.citizen_id)
    members = citizen.objects.filter(household_id=citi.household)
    return render(request, 'employee/empcitdetails.html', {'citizen': citi, 'household': household, 'land': land, 'senroll': senroll, 'vaccinations': vac, 'user': user, 'members': members})

class CitizenUpdateView(UpdateView):
    model = citizen
    fields = ['name', 'gender', 'dob', 'educational_qualification', 'household', 'parent', 'income']
    template_name = 'api/generic_form.html'
    
    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.object.citizen_id})

class HouseholdUpdateView(UpdateView):
    model = household
    fields = ['address', 'category', 'income']
    template_name = 'api/generic_form.html'

    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.object.citizen_id})

class LandUpdateView(UpdateView):
    model = land_records
    fields = ['area_acres', 'crop_type']
    template_name = 'api/generic_form.html'

    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.object.citizen_id})
    
class UserUpdateView(UpdateView):
    model = users
    fields = ['role', 'password_user']
    template_name = 'api/generic_form.html'

    def get_success_url(self):
        return reverse('emp_citizen_detail', kwargs={'citizen_id': self.object.user_id})
    
def add_land(request, citizen_id):
    if request.method == 'POST':
        form = LandForm(request.POST)
        if form.is_valid():
            land_id = form.cleaned_data['land_id']
            area_acres = form.cleaned_data['area_acres']
            crop_type = form.cleaned_data['crop_type']
            cit = citizen.objects.get(citizen_id=citizen_id)
            land = land_records(
                land_id=land_id,
                citizen_id=cit,
                area_acres=area_acres,
                crop_type=crop_type,
            )
            print("Form is valid")
            print(form.cleaned_data)
            land.save()
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
            cit = citizen.objects.get(citizen_id=citizen_id)
            vaccine = vaccinations(
                vaccination_id=vacc_id,
                citizen_id=cit,
                vaccine_type=vacc_type,
                date_administered=data_ad,
            )
            print("Form is valid")
            print(form.cleaned_data)
            vaccine.save()
            form = VaccineForm()
    else:
        form = VaccineForm()
    return render(request, 'employee/addvaccine.html', {'form': form})

@require_POST
def delete_land(request, land_id):
    try:
        land = land_records.objects.get(land_id=land_id)
        land.delete()
        return JsonResponse({'status': 'success'})
    except land_records.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Land record not found'}, status=404)
    
@require_POST
def delete_vaccine(request, vaccination_id):
    try:
        vaccine = vaccinations.objects.get(vaccination_id=vaccination_id)
        vaccine.delete()
        return JsonResponse({'status': 'success'})
    except vaccinations.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vaccine record not found'}, status=404)
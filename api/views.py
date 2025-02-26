from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import citizenSerializer
from .models import citizen, household, panchayat_employees, users
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection
from .forms import CitizenForm

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
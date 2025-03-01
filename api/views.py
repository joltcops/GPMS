from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import citizenSerializer
from .models import citizen, household, panchayat_employees, users, land_records, scheme_enrollments, welfare_schemes, assets, vaccinations, certificate, tax, census_data, env_data,benefit_application, certificate_application
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection
from .forms import CitizenForm, LandForm, VaccineForm, AssetsForm, CensusForm, WelfareForm, EnvForm, HouseForm, TaxForm, BenefitForm, CertificateForm,CertificateApprovalForm, BenefitApprovalForm, EmployeeForm
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import connection
from django.http import HttpResponseRedirect
from datetime import date
from django.db import IntegrityError, transaction
from django.contrib import messages
import re

def generate_new_citizen_id():
    last_applications = citizen.objects.values_list('citizen_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'C00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"C00{max_num + 1}"

    return new_id
def generate_new_census_data_id():
    last_applications = census_data.objects.values_list('census_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'CENSUS00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"CENSUS00{max_num + 1}"  

    return new_id
def generate_new_certificate_application_id():
    last_applications = certificate_application.objects.values_list('application_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'AP00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"AP00{max_num + 1}"  

    return new_id
def generate_new_benefit_application_id():
    last_applications = benefit_application.objects.values_list('application_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'BR00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"BR00{max_num + 1}"  

    return new_id
def generate_new_certificate_id():
    last_applications = certificate.objects.values_list('certificate_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'CERT00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"CERT00{max_num + 1}"  

    return new_id
def generate_new_scheme_enrollments_id():
    last_applications = scheme_enrollments.objects.values_list('enrollment_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'R00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"R00{max_num + 1}"  

    return new_id
def generate_new_land_records_id():
    last_applications = land_records.objects.values_list('land_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'L00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"L00{max_num + 1}"  

    return new_id
def generate_new_vaccinations_id():
    last_applications = vaccinations.objects.values_list('vaccination_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'V00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"V00{max_num + 1}"  

    return new_id
def generate_new_assets_id():
    last_applications = assets.objects.values_list('asset_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'A00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"A00{max_num + 1}"  

    return new_id
def generate_new_welfare_schemes_id():
    last_applications = welfare_schemes.objects.values_list('scheme_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'S00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"S00{max_num + 1}"  

    return new_id
def generate_new_tax_id():
    last_applications = tax.objects.values_list('tax_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'T00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"T00{max_num + 1}"  

    return new_id
def generate_new_env_data_id():
    last_applications = env_data.objects.values_list('record_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'REC00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"REC00{max_num + 1}"  

    return new_id
def generate_new_household_id():
    last_applications = household.objects.values_list('household_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'H00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"H00{max_num + 1}"  

    return new_id
def generate_new_panchayat_employees_id():
    last_applications = panchayat_employees.objects.values_list('employee_id', flat=True)

    # Extract numeric part using regex and find the maximum numeric value
    max_num = 0
    for app_id in last_applications:
        match = re.search(r'E00(\d+)', app_id)  # Extract digits after 'AP00'
        if match:
            num = int(match.group(1))  # Convert to integer
            max_num = max(max_num, num)  # Track max numeric value

    # Ensure the format remains AP00X (with two leading zeros before the number)
    new_id = f"E00{max_num + 1}"  

    return new_id

def add_citizen(request):
    if request.method == 'POST':
        form = CitizenForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    household_id = form.cleaned_data['household']
                    parent_id = form.cleaned_data['parent']
                    citizen_id = generate_new_citizen_id()
                    name = form.cleaned_data['name']
                    gender = form.cleaned_data['gender']
                    dob = form.cleaned_data['dob']
                    educational_qualification = form.cleaned_data['educational_qualification']
                    income = form.cleaned_data['income']

                    user_id = citizen_id
                    role = "CITIZEN"
                    password_user = '123456'

                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO users (user_id, role, password_user) VALUES (%s, %s, %s)", 
                                       [user_id, role, password_user])
                        cursor.execute("INSERT INTO citizen (citizen_id, name, gender, dob, educational_qualification, household_id, parent_id, income) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                                       [citizen_id, name, gender, dob, educational_qualification, household_id, parent_id, income])
                
                messages.success(request, 'Citizen added successfully.')
                form = CitizenForm()  # Reset the form after successful submission
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('citizen_id', 'A citizen with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the citizen. Please try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = CitizenForm()
    
    return render(request, 'employee/addcitizen.html', {'form': form})

def add_census_data(request):
    if request.method == 'POST':
        form = CensusForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    census_id = generate_new_census_data_id()
                    event_type = form.cleaned_data['event_type']
                    event_date = form.cleaned_data['event_date']
                    household_id = form.cleaned_data['household_id']
                    citizen_id = form.cleaned_data['citizen_id']

                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO census_data(census_id, household_id, citizen_id, event_type, event_date) VALUES (%s, %s, %s, %s, %s)",
                            [census_id, household_id, citizen_id, event_type, event_date]
                        )

                messages.success(request, 'Census data added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('census_id', 'A census record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the census data. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = CensusForm()
    
    return render(request, 'employee/addcensusdata.html', {'form': form})

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
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    application_id = generate_new_certificate_application_id()
                    certificate_type = form.cleaned_data['certificate_type']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO certificate_application (application_id, certificate_type, citizen_id, status) VALUES (%s, %s, %s, %s)",
                            [application_id, certificate_type, citizen_id, 'PENDING']
                        )

                messages.success(request, 'Certificate application submitted successfully.')
                # redirect to path('mycertificate/<str:citizen_id>/', views.mycertificate, name='my_certificates'),
                # return redirect('my_certificates', citizen_id=citizen_id)  # Redirect to a list of certificates or appropriate page
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('application_id', 'An application with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while submitting the application. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
        redirect('my_certificates', citizen_id=citizen_id)
    else:
        form = CertificateForm()
    
    return render(request, 'citizen/applycertificate.html', {'form': form})

def applybenefits(request, citizen_id):
    if request.method == 'POST':
        form = BenefitForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    application_id = generate_new_benefit_application_id()
                    scheme_id = form.cleaned_data['scheme_id']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO benefit_application (application_id, citizen_id, scheme_id, status) VALUES (%s, %s, %s, %s)",
                            [application_id, citizen_id, scheme_id, 'PENDING']
                        )

                messages.success(request, 'Benefit application submitted successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('application_id', 'An application with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while submitting the application. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = BenefitForm()
    
    return render(request, 'citizen/apply_benefit.html', {'form': form})

def view_cert_list(request):
    certs = certificate_application.objects.raw('SELECT * FROM certificate_application WHERE status = %s', ['PENDING'])
    return render(request, 'employee/certificate_list.html', {'certificates': certs})


def certificate_approve(request, application_id):
    if request.method == 'POST':
        form = CertificateApprovalForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    certificate_id = generate_new_certificate_id()
                    issue_date = form.cleaned_data['issue_date']
                    issuing_official = form.cleaned_data['issuing_official']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO certificate 
                            (certificate_id, certificate_type, applicant_id, issue_date, issuing_official) 
                            VALUES (%s, 
                                    (SELECT certificate_type FROM certificate_application WHERE application_id = %s), 
                                    (SELECT citizen_id FROM certificate_application WHERE application_id = %s), 
                                    %s, %s)
                            """,
                            [certificate_id, application_id, application_id, issue_date, issuing_official]
                        )
                        cursor.execute(
                            "UPDATE certificate_application SET status = %s WHERE application_id = %s",
                            ['APPROVED', application_id]
                        )

                messages.success(request, 'Certificate approved successfully.')
                return redirect('certificate_list')  # Redirect to a list of certificates or appropriate page
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('certificate_id', 'A certificate with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while approving the certificate. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = CertificateApprovalForm()
    
    return render(request, 'employee/certificate_approve.html', {'form': form, 'application_id': application_id})

def benefit_approve(request, application_id):
    if request.method == 'POST':
        form = BenefitApprovalForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    enrollment_id = generate_new_scheme_enrollments_id()
                    enrollment_date = form.cleaned_data['enrollment_date']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO scheme_enrollments 
                            (enrollment_id, citizen_id, scheme_id, enrollment_date) 
                            VALUES (%s, 
                                    (SELECT citizen_id FROM benefit_application WHERE application_id = %s), 
                                    (SELECT scheme_id FROM benefit_application WHERE application_id = %s), 
                                    %s)
                            """,
                            [enrollment_id, application_id, application_id, enrollment_date]
                        )
                        cursor.execute(
                            "UPDATE benefit_application SET status = %s WHERE application_id = %s",
                            ['APPROVED', application_id]
                        )

                messages.success(request, 'Benefit application approved successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('enrollment_id', 'An enrollment with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while approving the benefit. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = BenefitApprovalForm()
    
    return render(request, 'employee/benefit_approve.html', {'form': form, 'application_id': application_id})
    
def view_bene_list(request):
    bene = benefit_application.objects.raw('SELECT * FROM benefit_application WHERE status = %s', ['PENDING'])
    return render(request, 'employee/benefit_list.html', {'benefits': bene})

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
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM tax WHERE payer_id = %s', [citizen_id])
        taxes = cursor.fetchall()
    return render(request, 'employee/empcitdetails.html', {'citizen': citi, 'household': house, 'land': land, 'senroll': senroll, 'vaccinations': vac, 'user': user, 'members': members, 'taxes': taxes})

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

class SchemeUpdateView(UpdateView):
    model = welfare_schemes
    fields = ['name', 'description']
    template_name = 'api/generic_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        scheme_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE welfare_schemes
                SET name = %s, description = %s
                WHERE scheme_id = %s
            ''', [data['name'], data['description'], scheme_id])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('welfare_schemes_list')
    
class CenUpdateView(UpdateView):
    model = census_data
    fields = ['event_type', 'event_date']
    template_name = 'api/generic_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        cen_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE census_data
                SET event_type = %s, event_date = %s
                WHERE census_id = %s
            ''', [data['event_type'], data['event_date'], cen_id])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('census_data_list')


def add_land(request, citizen_id):
    if request.method == 'POST':
        form = LandForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    land_id = generate_new_land_records_id()
                    area_acres = form.cleaned_data['area_acres']
                    crop_type = form.cleaned_data['crop_type']
                    
                    cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO land_records (land_id, citizen_id, area_acres, crop_type) VALUES (%s, %s, %s, %s)",
                            [land_id, cit.citizen_id, area_acres, crop_type]
                        )

                messages.success(request, 'Land record added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('land_id', 'A land record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the land record. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = LandForm()
    
    return render(request, 'employee/addland.html', {'form': form, 'citizen_id': citizen_id})
def add_vaccine(request, citizen_id):
    if request.method == 'POST':
        form = VaccineForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    vacc_id = generate_new_vaccinations_id()
                    vacc_type = form.cleaned_data['vaccine_type']
                    data_ad = form.cleaned_data['date_administered']
                    
                    cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO vaccinations (vaccination_id, citizen_id, vaccine_type, date_administered) VALUES (%s, %s, %s, %s)",
                            [vacc_id, cit.citizen_id, vacc_type, data_ad]
                        )

                messages.success(request, 'Vaccination record added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('vaccination_id', 'A vaccination record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the vaccination record. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = VaccineForm()
    
    return render(request, 'employee/addvaccine.html', {'form': form, 'citizen_id': citizen_id})

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

def add_assets(request):
    if request.method == 'POST':
        form = AssetsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    asset_id = generate_new_assets_id()
                    type = form.cleaned_data['type']
                    location = form.cleaned_data['location']
                    installation_date = form.cleaned_data['installation_date']
                    budget = form.cleaned_data['budget']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO assets (asset_id, type, location, installation_date, budget) VALUES (%s, %s, %s, %s, %s)",
                            [asset_id, type, location, installation_date, budget]
                        )

                messages.success(request, 'Asset added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('asset_id', 'An asset with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the asset. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = AssetsForm()
    
    return render(request, 'employee/addassets.html', {'form': form})

def add_welfare_schemes(request):
    if request.method == 'POST':
        form = WelfareForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    scheme_id = generate_new_welfare_schemes_id()
                    name = form.cleaned_data['name']
                    description = form.cleaned_data['description']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO welfare_schemes (scheme_id, name, description) VALUES (%s, %s, %s)",
                            [scheme_id, name, description]
                        )

                messages.success(request, 'Welfare scheme added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('scheme_id', 'A welfare scheme with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the welfare scheme. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = WelfareForm()
    
    return render(request, 'employee/addwelfareschemes.html', {'form': form})

@require_POST
def delete_asset(request, asset_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM assets WHERE asset_id = %s", [asset_id])
        return JsonResponse({'status': 'success'})
    except vaccinations.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Asset record not found'}, status=404)
    
@require_POST
def delete_scheme(request, scheme_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM welfare_schemes WHERE scheme_id = %s", [scheme_id])
        return JsonResponse({'status': 'success'})
    except welfare_schemes.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Welfare scheme not found'}, status=404)
@require_POST
def delete_cen(request, cen_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM census_data WHERE census_id = %s", [cen_id])
        return JsonResponse({'status': 'success'})
    except census_data.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Census data not found'}, status=404)
    
class AssetUpdateView(UpdateView):
    model = assets
    fields = [ 'type', 'location', 'installation_date', 'budget']
    template_name = 'api/generic_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        asset_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE assets
                SET  type = %s, location = %s, 
                    installation_date = %s, budget = %s 
                WHERE asset_id = %s
            ''', [data['type'], data['location'], data['installation_date'],
                  data['budget'], asset_id])

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('assetslist')

def census_data_list(request):
    census = census_data.objects.raw('SELECT * FROM census_data')
    return render(request, 'employee/census_data_list.html', {'census_data': census})

def welfare_schemes_list(request):
    schemes = welfare_schemes.objects.raw('SELECT * FROM welfare_schemes')
    return render(request, 'employee/welfare_schemes_list.html', {'schemes': schemes})

class EnvUpdateView(UpdateView):
    model = env_data
    fields = ['rainfall', 'aqi', 'gwl', 'date_of_record', 'temperature', 'humidity', 'wind_speed']
    template_name = 'api/generic_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        record_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE env_data
                SET rainfall = %s, aqi = %s, gwl = %s, 
                    date_of_record = %s, temperature = %s, 
                    humidity = %s, wind_speed = %s
                WHERE record_id = %s
            ''', [data['rainfall'], data['aqi'], data['gwl'], data['date_of_record'],
                  data['temperature'], data['humidity'], data['wind_speed'], record_id])

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('env_list')
    
class HouseUpdateView(UpdateView):
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
        return reverse('house_list')

def add_tax(request, citizen_id):
    if request.method == 'POST':
        form = TaxForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tax_id = generate_new_tax_id()
                    payer_id = citizen_id
                    type = form.cleaned_data['type']
                    amount = form.cleaned_data['amount']
                    due_date = form.cleaned_data['due_date']
                    paid_status = form.cleaned_data['paid_status']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO tax (tax_id, payer_id, type, amount, due_date, paid_status) VALUES (%s, %s, %s, %s, %s, %s)",
                            [tax_id, payer_id, type, amount, due_date, paid_status]
                        )

                messages.success(request, 'Tax record added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('tax_id', 'A tax record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the tax record. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = TaxForm()
    
    return render(request, 'employee/addtax.html', {'form': form, 'citizen_id': citizen_id})

def env_list(request):
    env = env_data.objects.raw('SELECT * FROM env_data')
    return render(request, 'employee/envlist.html', {'env': env})

def house_list(request):
    houses = household.objects.raw('SELECT * FROM household')
    return render(request, 'employee/houses.html', {'houses': houses})

def add_env(request):
    if request.method == 'POST':
        form = EnvForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    record_id = generate_new_env_data_id()
                    rainfall = form.cleaned_data['rainfall']
                    aqi = form.cleaned_data['aqi']
                    gwl = form.cleaned_data['gwl']
                    date_of_record = form.cleaned_data['date_of_record']
                    temperature = form.cleaned_data['temperature']
                    humidity = form.cleaned_data['humidity']
                    wind_speed = form.cleaned_data['wind_speed']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO env_data (record_id, rainfall, aqi, gwl, date_of_record, temperature, humidity, wind_speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            [record_id, rainfall, aqi, gwl, date_of_record, temperature, humidity, wind_speed]
                        )

                messages.success(request, 'Environmental data added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('record_id', 'A record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the environmental data. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = EnvForm()
    
    return render(request, 'employee/addenv.html', {'form': form})

def add_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    household_id = generate_new_household_id()
                    address = form.cleaned_data['address']
                    category = form.cleaned_data['category']
                    income = form.cleaned_data['income']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO household (household_id, address, category, income) VALUES (%s, %s, %s, %s)",
                            [household_id, address, category, income]
                        )

                messages.success(request, 'Household added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('household_id', 'A household with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the household. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = HouseForm()
    
    return render(request, 'employee/addhouse.html', {'form': form})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    employee_id = generate_new_panchayat_employees_id()
                    citizen_id = form.cleaned_data['citizen_id']
                    department = form.cleaned_data['department']
                    role = form.cleaned_data['role']
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO users (user_id, role, password_user) VALUES (%s, %s, %s)",
                            [employee_id, role, '123456']
                        )
                        cursor.execute(
                            "INSERT INTO panchayat_employees (employee_id, citizen_id, role, department) VALUES (%s, %s, %s, %s)",
                            [employee_id, citizen_id, role, department]
                        )

                messages.success(request, 'Employee added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('employee_id', 'An employee with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the employee. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = EmployeeForm()
    
    return render(request, 'admin/addemployee.html', {'form': form})

def admhome(request):
    return render(request, 'admin/admhome.html')

def admempdetails(request, employee_id):
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees WHERE employee_id = %s', [employee_id])[0]
    cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [emp.citizen_id.citizen_id])[0]
    user = users.objects.raw('SELECT * FROM users WHERE user_id = %s', [employee_id])[0]
    return render(request, 'admin/admempdetails.html', {'emp': emp, 'cit': cit, 'user': user})

def employee_list(request):
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees')
    return render(request, 'admin/employee_list.html', {'employees': emp})

def delete_employee(request, employee_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", [employee_id])
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

class EmployeeUpdateView(UpdateView):
    model = panchayat_employees
    fields = ['citizen_id', 'role', 'department']
    template_name = 'api/generic_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        employee_id = self.kwargs['pk']
        citizen_id = data['citizen_id'].citizen_id if data['citizen_id'] else None
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE panchayat_employees
                SET  citizen_id = %s,  role = %s, department = %s
                WHERE employee_id = %s
            ''', [citizen_id, data['role'], data['department'], employee_id])

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('adm_employee_detail', kwargs={'employee_id': self.kwargs['pk']})
    
class EmpUserUpdateView(UpdateView):
    model = users
    fields = ['password_user']
    template_name = 'api/generic_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        user_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('''
                UPDATE users
                SET password_user = %s
                WHERE user_id = %s
            ''', [data['password_user'], user_id])

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('adm_employee_detail', kwargs={'employee_id': self.object.user_id})

class EmpCitUpdateView(UpdateView):
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
        emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees WHERE citizen_id = %s', [self.object.citizen_id])[0]
        return reverse('adm_employee_detail', kwargs={'employee_id': emp.employee_id})

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from .models import citizen, household, panchayat_employees, users, land_records, scheme_enrollments, welfare_schemes, assets, vaccinations, certificate, tax, census_data, env_data,benefit_application, certificate_application
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection
from .forms import CitizenForm, LandForm, VaccineForm, AssetsForm, CensusForm, WelfareForm, EnvForm, HouseForm, TaxForm, EmployeeForm, EnvDateForm, EnvValueForm, InfraDateForm, InfraLocForm, AgriIncome, AgriArea, CensusDateForm, CensusYearForm, CensusPopForm, SchemeDateForm, SchemeNameForm
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date
import re
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.models import User as auth_user
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login, logout
from django.utils.timezone import now

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

def create_user(username, password, role):
    """
    Creates a user in Django's built-in User model.
    """
    try:
        user = User.objects.create_user(username=username, password=password)
        user.is_active = True  # Activate the user
        if role == 'ADMIN':
            user.is_staff = True
            user.is_superuser = True
        user.save()
        return user
    except IntegrityError:
        print("User with this ID already exists.")
        return None  # Handle duplicate username case

def add_citizen(request, employee_id):
    if request.user.is_anonymous:
        return redirect("/api/login_page")
    
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

                    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]

                    user_id = citizen_id
                    role = "CITIZEN"
                    password_user = '123456$@'  # Default password (should be changed by user)

                    # **Step 1: Create user in Django's User model**
                    user = create_user(user_id, password_user, role)
                    if user is None:
                        form.add_error(None, "User with this ID already exists in the system.")
                        return render(request, 'employee/addcitizen.html', {'form': form, 'emp': employee})

                    # **Step 2: Insert into the custom users & citizen table**
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO users (user_id, role, password_user) VALUES (%s, %s, %s)", 
                                       [user_id, role, password_user])
                        cursor.execute("INSERT INTO citizen (citizen_id, name, gender, dob, educational_qualification, household_id, parent_id, income) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                                       [citizen_id, name, gender, dob, educational_qualification, household_id, parent_id, income])
                
                messages.success(request, 'Citizen added successfully.')
                form = CitizenForm()

            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('citizen_id', 'A citizen with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the citizen. Please try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = CitizenForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]

    return render(request, 'employee/addcitizen.html', {'form': form, 'emp': employee})

def add_census_data(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = CensusForm()
                # messages.success(request, 'Census data added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('census_id', 'A census record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the census data. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = CensusForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addcensusdata.html', {'form': form, 'emp': employee})

def home_page(request):
    # if(request.user.is_anonymous):
    #     return redirect("/api/login_page")
    return render(request, 'index.html')

def citizen_list(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citizens = citizen.objects.raw('SELECT * FROM citizen order by citizen_id')
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/citizen_list.html', {'citizens': citizens, 'emp': employee})

def citizen_detail(request, citizen_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    members = citizen.objects.raw('SELECT * FROM citizen WHERE household_id = (SELECT household_id from citizen where citizen_id = %s)', [citizen_id])
    return render(request, 'citizen/citizen_detail.html', {'citizen': citi, 'members': members})

def household_citdetails(request, citizen_id, parent_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    par = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [parent_id])[0]
    return render(request, 'citizen/household_citizen.html', {'citizen': citi, 'parent': par})

def cithome(request, citizen_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    return render(request, 'citizen/citizenhome.html', {'citizen': citi})

def mycertificate(request, citizen_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM certificate WHERE applicant_id = %s', [citizen_id])
        certs = cursor.fetchall()
    return render(request, 'citizen/certificate.html', {'citizen': citi, 'certificates': certs})

def mybenefits(request, citizen_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    schemes = scheme_enrollments.objects.raw('SELECT * FROM scheme_enrollments WHERE citizen_id = %s', [citizen_id])
    all_schemes = welfare_schemes.objects.raw('SELECT * FROM welfare_schemes')
    return render(request, 'citizen/benefits.html', {'citizen': citi, 'schemes': schemes, 'all': all_schemes})

def mytax(request, citizen_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tax WHERE payer_id = %s and paid_status='DUE' order by due_date desc", [citizen_id])
        tax_due = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tax WHERE payer_id = %s and paid_status='PAID' order by due_date desc", [citizen_id])
        tax_paid = cursor.fetchall()

    return render(request, 'citizen/tax.html', {'citizen': citi, 'tax_due': tax_due, 'tax_paid': tax_paid})


@require_POST
def applycertificate(request, citizen_id, certificate_type):
    if request.user.is_anonymous:
        return redirect("/api/login_page")
    
    try:
        with connection.cursor() as cursor:
            # Check if the citizen already has an approved certificate of this type
            cursor.execute(
                "SELECT COUNT(*) FROM certificate_application WHERE citizen_id = %s AND certificate_type = %s AND status = 'APPROVED'",
                [citizen_id, certificate_type]
            )
            approved_count = cursor.fetchone()[0]

            # Check if the citizen already has a pending application for this certificate type
            cursor.execute(
                "SELECT COUNT(*) FROM certificate_application WHERE citizen_id = %s AND certificate_type = %s AND status = 'PENDING'",
                [citizen_id, certificate_type]
            )
            pending_count = cursor.fetchone()[0]

        if approved_count > 0:
            return JsonResponse({'status': 'error', 'message': 'You already have this certificate.'}, status=400)

        if pending_count > 0:
            return JsonResponse({'status': 'error', 'message': 'You already have a pending application for this certificate.'}, status=400)

        # If no conflicts, proceed with application
        with transaction.atomic():
            application_id = generate_new_certificate_application_id()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO certificate_application (application_id, certificate_type, citizen_id, status) VALUES (%s, %s, %s, %s)",
                    [application_id, certificate_type, citizen_id, 'PENDING']
                )

        messages.success(request, 'Certificate application submitted successfully.')
        return JsonResponse({'status': 'success', 'message': 'Certificate application submitted successfully.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)


@require_POST
def applybenefits(request, citizen_id, scheme_id):
    if request.user.is_anonymous:
        return redirect("/api/login_page")
    
    try:
        with connection.cursor() as cursor:
            # Check if the citizen is already enrolled in this scheme
            cursor.execute(
                "SELECT COUNT(*) FROM benefit_application WHERE citizen_id = %s AND scheme_id = %s AND status = 'APPROVED'",
                [citizen_id, scheme_id]
            )
            approved_count = cursor.fetchone()[0]

            # Check if there is a pending application
            cursor.execute(
                "SELECT COUNT(*) FROM benefit_application WHERE citizen_id = %s AND scheme_id = %s AND status = 'PENDING'",
                [citizen_id, scheme_id]
            )
            pending_count = cursor.fetchone()[0]

        if approved_count > 0:
            return JsonResponse({'status': 'error', 'message': 'You are already enrolled in this benefit scheme.'}, status=400)

        if pending_count > 0:
            return JsonResponse({'status': 'error', 'message': 'You already have a pending application for this benefit scheme.'}, status=400)

        # Proceed with application if no conflicts
        with transaction.atomic():
            application_id = generate_new_benefit_application_id()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO benefit_application (application_id, citizen_id, scheme_id, status) VALUES (%s, %s, %s, %s)",
                    [application_id, citizen_id, scheme_id, 'PENDING']
                )

        messages.success(request, 'Benefit application submitted successfully.')
        return JsonResponse({'status': 'success', 'message': 'Benefit application submitted successfully.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)


def view_cert_list(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    certs = certificate_application.objects.raw('SELECT * FROM certificate_application WHERE status = %s', ['PENDING'])
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/certificate_list.html', {'certificates': certs, 'emp': employee})

def certificate_approve(request, application_id, employee_id):
    if request.user.is_anonymous:
        return redirect("/api/login_page")

    try:
        with transaction.atomic():
            certificate_id = generate_new_certificate_id()
            issue_date = now().date()  # Get current date
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO certificate 
                    (certificate_id, certificate_type, applicant_id, issue_date, issuing_official) 
                    VALUES (
                        %s, 
                        (SELECT certificate_type FROM certificate_application WHERE application_id = %s), 
                        (SELECT citizen_id FROM certificate_application WHERE application_id = %s), 
                        %s, %s
                    )
                    """,
                    [certificate_id, application_id, application_id, issue_date, employee_id]
                )
                cursor.execute(
                    "UPDATE certificate_application SET status = %s WHERE application_id = %s",
                    ['APPROVED', application_id]
                )

        messages.success(request, 'Certificate approved successfully.')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')

    return redirect('certificate_list', employee_id=employee_id)

def benefit_approve(request, application_id, employee_id):
    if request.user.is_anonymous:
        return redirect("/api/login_page")

    try:
        with transaction.atomic():
            enrollment_id = generate_new_scheme_enrollments_id()
            enrollment_date = now().date()  # Use current date
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO scheme_enrollments 
                    (enrollment_id, citizen_id, scheme_id, enrollment_date) 
                    VALUES (
                        %s, 
                        (SELECT citizen_id FROM benefit_application WHERE application_id = %s), 
                        (SELECT scheme_id FROM benefit_application WHERE application_id = %s), 
                        %s
                    )
                    """,
                    [enrollment_id, application_id, application_id, enrollment_date]
                )
                cursor.execute(
                    "UPDATE benefit_application SET status = %s WHERE application_id = %s",
                    ['APPROVED', application_id]
                )

        messages.success(request, 'Benefit application approved successfully.')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')

    return redirect('benefits_list', employee_id=employee_id)

    
def view_bene_list(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    bene = benefit_application.objects.raw('SELECT * FROM benefit_application WHERE status = %s', ['PENDING'])
    return render(request, 'employee/benefit_list.html', {'benefits': bene, 'emp':employee})

def logout(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    return render(request, 'logout.html')

def emphome(request, emp_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees WHERE employee_id = %s', [emp_id])[0]
    return render(request, 'employee/emphome.html', {'emp': emp})

def empdetail(request, emp_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees WHERE employee_id = %s', [emp_id])[0]
    cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [emp.citizen_id.citizen_id])[0]
    print(emp.employee_id)
    return render(request, 'employee/empdetail.html', {'emp': emp, 'cit': cit})

def empcitdetails(request, citizen_id, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    citi = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [citizen_id])[0]
    house = household.objects.raw('SELECT * FROM household join citizen using (household_id) WHERE citizen_id = %s', [citizen_id])[0]
    land = land_records.objects.raw('SELECT * FROM land_records WHERE citizen_id = %s', [citizen_id])
    senroll = scheme_enrollments.objects.raw('SELECT * FROM scheme_enrollments WHERE citizen_id = %s', [citizen_id])
    vac = vaccinations.objects.raw('SELECT * FROM vaccinations WHERE citizen_id = %s', [citizen_id])
    user = users.objects.raw('SELECT * FROM users join citizen ON users.user_id = citizen.citizen_id WHERE citizen.citizen_id = %s', [citizen_id])[0]
    members = citizen.objects.raw('SELECT * FROM citizen WHERE household_id = (SELECT household_id from citizen where citizen_id = %s)', [citizen_id])
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM tax WHERE payer_id = %s', [citizen_id])
        taxes = cursor.fetchall()
    return render(request, 'employee/empcitdetails.html', {'citizen': citi, 'household': house, 'land': land, 'senroll': senroll, 'vaccinations': vac, 'user': user, 'members': members, 'taxes': taxes, 'emp': employee})

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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})

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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})


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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})

    
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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})

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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})
    
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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})


def add_land(request, citizen_id, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = LandForm()
                # messages.success(request, 'Land record added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('land_id', 'A land record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the land record. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = LandForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addland.html', {'form': form, 'citizen_id': citizen_id, 'emp':employee})
def add_vaccine(request, citizen_id, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = VaccineForm()
                # messages.success(request, 'Vaccination record added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('vaccination_id', 'A vaccination record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the vaccination record. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = VaccineForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addvaccine.html', {'form': form, 'citizen_id': citizen_id, 'emp':employee})

@require_POST
def delete_land(request, land_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM land_records WHERE land_id = %s", [land_id])
        return JsonResponse({'status': 'success'})
    except land_records.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Land record not found'}, status=404)
    
@require_POST
def delete_tax(request, tax_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tax WHERE tax_id = %s", [tax_id])
        return JsonResponse({'status': 'success'})
    except land_records.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Land record not found'}, status=404)
    
@require_POST
def delete_scheme_enrollment(request, enrollment_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM scheme_enrollments WHERE enrollment_id = %s", [enrollment_id])
        return JsonResponse({'status': 'success'})
    except land_records.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Land record not found'}, status=404)
    
@require_POST
def delete_vaccine(request, vaccination_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM vaccinations WHERE vaccination_id = %s", [vaccination_id])
        return JsonResponse({'status': 'success'})
    except vaccinations.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vaccine record not found'}, status=404)
    
def remove_user(user_id):
    """
    Removes a user from Django's built-in User model.
    """
    try:
        user = User.objects.get(username=user_id)
        user.delete()
        return True
    except User.DoesNotExist:
        return False

@require_POST
def delete_citizen(request, citizen_id):
    if request.user.is_anonymous:
        return redirect("/api/login_page")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", [citizen_id])

        # Remove the user from Django's built-in User model
        user_deleted = remove_user(citizen_id)

        return JsonResponse({'success': True, 'user_deleted': user_deleted})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def assetslist(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    asset = assets.objects.raw('SELECT * FROM assets')
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/assets_list.html', {'assets': asset, 'emp':employee})

def add_assets(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = AssetsForm()
                # messages.success(request, 'Asset added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('asset_id', 'An asset with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the asset. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = AssetsForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addassets.html', {'form': form, 'emp':employee})

def add_welfare_schemes(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = WelfareForm()
                # messages.success(request, 'Welfare scheme added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('scheme_id', 'A welfare scheme with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the welfare scheme. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = WelfareForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addwelfareschemes.html', {'form': form, 'emp':employee})

@require_POST
def delete_asset(request, asset_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM assets WHERE asset_id = %s", [asset_id])
        return JsonResponse({'status': 'success'})
    except vaccinations.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Asset record not found'}, status=404)
    
@require_POST
def delete_scheme(request, scheme_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM welfare_schemes WHERE scheme_id = %s", [scheme_id])
        return JsonResponse({'status': 'success'})
    except welfare_schemes.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Welfare scheme not found'}, status=404)
@require_POST
def delete_cen(request, cen_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})

def census_data_list(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    census = census_data.objects.raw('SELECT * FROM census_data')
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/census_data_list.html', {'census_data': census, 'emp': employee})

def welfare_schemes_list(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    schemes = welfare_schemes.objects.raw('SELECT * FROM welfare_schemes')
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/welfare_schemes_list.html', {'schemes': schemes, 'emp': employee})

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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})
    
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
        return reverse('emp_home', kwargs={'emp_id': self.kwargs['pkk']})

def add_tax(request, citizen_id, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = TaxForm()
                # messages.success(request, 'Tax record added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('tax_id', 'A tax record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the tax record. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = TaxForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addtax.html', {'form': form, 'citizen_id': citizen_id, 'emp':employee})

def env_list(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    env = env_data.objects.raw('SELECT * FROM env_data')
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/envlist.html', {'env': env, 'emp': employee})

def house_list(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    houses = household.objects.raw('SELECT * FROM household')
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/houses.html', {'houses': houses, 'emp':employee})

def add_env(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = EnvForm()
                # messages.success(request, 'Environmental data added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('record_id', 'A record with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the environmental data. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = EnvForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addenv.html', {'form': form, 'emp':employee})

def add_house(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
                form = HouseForm()
                # messages.success(request, 'Household added successfully.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('household_id', 'A household with this ID already exists.')
                else:
                    form.add_error(None, 'An error occurred while adding the household. Please check all fields and try again.')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
    else:
        form = HouseForm()
    employee = panchayat_employees.objects.raw("SELECT * FROM panchayat_employees where employee_id = %s", [employee_id])[0]
    return render(request, 'employee/addhouse.html', {'form': form, 'emp':employee})

def add_employee(request):
    if request.user.is_anonymous:
        return redirect("/api/login_page")

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    employee_id = generate_new_panchayat_employees_id()
                    print("Generated Employee ID:", employee_id)
                    citizen_id = form.cleaned_data['citizen_id']
                    department = form.cleaned_data['department']
                    role = form.cleaned_data['role']
                    password = '123456$@'  # Default password

                    # Create user in Django User model
                    user = create_user(employee_id, password, role)
                    if not user:
                        form.add_error(None, 'A user with this ID already exists.')
                        raise IntegrityError("User creation failed due to duplicate ID.")
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO users (user_id, role, password_user) VALUES (%s, %s, %s)",
                            [employee_id, 'EMPLOYEE', password]
                        )

                    citi = citizen.objects.get(citizen_id=citizen_id)
                    panchayat_employees.objects.create(
                        employee_id=employee_id, citizen_id=citi,
                        role=role, department=department
                    )

                messages.success(request, 'Employee added successfully.')
                return redirect('adm_home')

            except citizen.DoesNotExist:
                form.add_error('citizen_id', 'No citizen found with this ID.')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('employee_id', 'An employee with this ID already exists.')
                else:
                    form.add_error(None, f'Database integrity error: {str(e)}')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
                print(f"Unexpected error: {str(e)}")  # Log the full error

    else:
        form = EmployeeForm()

    return render(request, 'admin/addemployee.html', {'form': form})


def admhome(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    return render(request, 'admin/admhome.html')

def admempdetails(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees WHERE employee_id = %s', [employee_id])[0]
    cit = citizen.objects.raw('SELECT * FROM citizen WHERE citizen_id = %s', [emp.citizen_id.citizen_id])[0]
    user = users.objects.raw('SELECT * FROM users WHERE user_id = %s', [employee_id])[0]
    return render(request, 'admin/admempdetails.html', {'emp': emp, 'cit': cit, 'user': user})

def employee_list(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    emp = panchayat_employees.objects.raw('SELECT * FROM panchayat_employees')
    return render(request, 'admin/employee_list.html', {'employees': emp})

def delete_employee(request, employee_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
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
        return reverse('adm_home')
    
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
        return reverse('adm_home')

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
        return reverse('adm_home')
    

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def getschemes(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    schemes=welfare_schemes.objects.all()
    return render(request, 'govmonitor/schemes.html', {'schemes': schemes, "user_id":user_id, "password":password})

def getschemes_gen(request):
    # if(request.user.is_anonymous):
    #     return redirect("/api/login_page")
    schemes=welfare_schemes.objects.all()
    return render(request, 'general/schemes_gen.html', {'schemes': schemes})

def show_date_scheme(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = SchemeDateForm()
    records = None

    if request.method == 'POST':
        form = SchemeDateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            with connection.cursor() as cursor:
                cursor.execute("SELECT welfare_schemes.name, COUNT(*) FROM citizen JOIN scheme_enrollments ON citizen.citizen_id = scheme_enrollments.citizen_id JOIN welfare_schemes ON scheme_enrollments.scheme_id = welfare_schemes.scheme_id WHERE enrollment_date>=%s AND enrollment_date<=%s GROUP BY welfare_schemes.name;", [start_date, end_date])
                records = cursor.fetchall()

    return render(request, "govmonitor/show_date_scheme.html", {"form":form, "records":records, "userid":userid, "password":password})

def show_stat_scheme(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = SchemeNameForm()
    records = None
    edu = None

    if request.method == 'POST':
        form = SchemeNameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*), AVG(income) FROM citizen JOIN scheme_enrollments ON citizen.citizen_id = scheme_enrollments.citizen_id JOIN welfare_schemes ON welfare_schemes.scheme_id = scheme_enrollments.scheme_id WHERE welfare_schemes.name = %s;", [name])
                records = cursor.fetchall()

                cursor.execute("SELECT welfare_schemes.name, citizen.educational_qualification, COUNT(*) FROM citizen JOIN scheme_enrollments ON citizen.citizen_id = scheme_enrollments.citizen_id JOIN welfare_schemes ON welfare_schemes.scheme_id = scheme_enrollments.scheme_id WHERE welfare_schemes.name = %s GROUP BY welfare_schemes.name, citizen.educational_qualification;", [name])
                edu = cursor.fetchall()

    return render(request, "govmonitor/show_stat_scheme.html", {"form":form, "records":records, "edu":edu, "userid":userid, "password":password})


def panchayat_details(request):
    # if(request.user.is_anonymous):
    #     return redirect("/api/login_page")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT name, role, department FROM citizen, panchayat_employees WHERE citizen.citizen_id=panchayat_employees.citizen_id")  # Query only required fields
        results = cursor.fetchall()
    return render(request, 'general/panchayat_details.html', {'employee': results})

def show_general_env(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    user_id = request.GET.get("user_id")  # Retrieve user_id from query parameters
    password = request.GET.get("password")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT AVG(rainfall), AVG(aqi), AVG(gwl), AVG(temperature),
                   AVG(humidity), AVG(wind_speed)
            FROM env_data;
        """)
        result = cursor.fetchone()  # Fetch a single row

    # Check if result is None (in case the table is empty)
    if result is None or all(v is None for v in result):
        return render(request, "govmonitor/general_env.html", {"error": "No data available", "user_id": user_id, "password": password})

    # Convert the tuple to a dictionary
    data = {
        "avg_rainfall": result[0],
        "avg_aqi": result[1],
        "avg_gwl": result[2],
        "avg_temperature": result[3],
        "avg_humidity": result[4],
        "avg_wind_speed": result[5]
    }

    return render(request, "govmonitor/general_env.html", {"data": data, "user_id": user_id, "password": password})


def show_general_env_1(request):
    # if(request.user.is_anonymous):
    #     return redirect("/api/login_page")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT AVG(rainfall), AVG(aqi), AVG(gwl), AVG(temperature),
                   AVG(humidity), AVG(wind_speed)
            FROM env_data;
        """)
        result = cursor.fetchone()  # Fetch a single row

    # Check if result is None (in case the table is empty)
    if result is None or all(v is None for v in result):
        return render(request, "general/general_env_1.html", {"error": "No data available"})

    # Convert the tuple to a dictionary
    data = {
        "avg_rainfall": result[0],
        "avg_aqi": result[1],
        "avg_gwl": result[2],
        "avg_temperature": result[3],
        "avg_humidity": result[4],
        "avg_wind_speed": result[5]
    }

    return render(request, "general/general_env_1.html", {"data": data})


def show_date_env(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = EnvDateForm()  # Initialize the form for GET request
    records = None  # Default value for records

    if request.method == 'POST':
        form = EnvDateForm(request.POST)  # Bind form data
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
           
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM env_data
                    WHERE date_of_record >= %s AND date_of_record <= %s;
                """, [start_date, end_date])
               
                records = cursor.fetchall()  # Fetch all matching records

    return render(request, "govmonitor/show_date_env.html", {"form": form, "records": records, "userid":userid, "password":password})

def show_val_env(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = EnvValueForm()  # Initialize the form for GET request
    records = None  # Default value for records

    if request.method == 'POST':
        form = EnvValueForm(request.POST)  # Bind form data
        if form.is_valid():
            # Extract form values
            t = form.cleaned_data['temperature']
            a = form.cleaned_data['air_quality_index']
            g = form.cleaned_data['ground_water_level']
            h = form.cleaned_data['humidity']
            r = form.cleaned_data['rainfall']
           
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM env_data
                    WHERE temperature >= %s OR aqi >= %s OR gwl >= %s OR humidity >= %s OR rainfall >= %s;
                """, [t, a, g, h, r])
               
                records = cursor.fetchall()  # Fetch all matching records

    return render(request, "govmonitor/show_val_env.html", {"form": form, "records": records, "userid":userid, "password":password})

def show_above_avg_env(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    parameters = {
        "temperature": "Temperature",
        "aqi": "Air Quality Index",
        "gwl": "Ground Water Level",
        "humidity": "Humidity",
        "rainfall": "Rainfall"
    }

    selected_param = None
    records = None  # Default value for records

    if request.method == "POST":
        selected_param = request.POST.get("parameter")

        if selected_param in parameters:
            with connection.cursor() as cursor:
                # Fetch the average value for the selected parameter
                cursor.execute(f"SELECT AVG({selected_param}) FROM env_data;")
                avg_value = cursor.fetchone()[0]  # Extract the single value

                if avg_value is not None:
                    # Fetch all records where the parameter value is above its average
                    cursor.execute(f"SELECT * FROM env_data WHERE {selected_param} > %s;", [avg_value])
                    records = cursor.fetchall()

    return render(request, "govmonitor/show_above_avg_env.html", {"parameters": parameters, "selected_param": selected_param, "records": records, "userid":userid, "password":password})

def infrastructure_data(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT SUM(budget), AVG(budget), MAX(budget), MIN(budget) FROM assets;")
        results = cursor.fetchall()
    return render(request, 'govmonitor/infrastructure_data.html', {'asset_records':results, "user_id":user_id, "password":password})

def show_date_infra(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = InfraDateForm()
    records=None
    avg_budget = None
    sum_budget = None

    if request.method == 'POST':
        form = InfraDateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM assets WHERE installation_date>=%s AND installation_date<=%s;", [start_date, end_date])
                records = cursor.fetchall()

            # Query to get the budget summary
                cursor.execute("SELECT AVG(budget), SUM(budget) FROM assets WHERE installation_date>=%s AND installation_date<=%s;", [start_date, end_date])
                summary = cursor.fetchone()

                if summary:
                    avg_budget = summary[0]  # Extract AVG(budget)
                    sum_budget = summary[1]  # Extract SUM(budget)
               
    return render(request, "govmonitor/show_date_infra.html", {
        "form": form,
        "records": records,
        "avg_budget": avg_budget,
        "sum_budget": sum_budget,
        "userid":userid,
        "password":password
    })

def show_loc_infra(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = InfraLocForm()
    records = None
    avg_budget = None
    sum_budget = None

    if request.method == 'POST':
        form = InfraLocForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            type = form.cleaned_data['type']

            with connection.cursor() as cursor:
                # Query to fetch the filtered records
                cursor.execute("""
                    SELECT *
                    FROM assets
                    WHERE location=%s AND type=%s;
                """, [location, type])
                records = cursor.fetchall()

                # Query to get the budget summary
                cursor.execute("""
                    SELECT AVG(budget), SUM(budget)
                    FROM assets
                    WHERE location=%s AND type=%s;
                """, [location, type])
                summary = cursor.fetchone()

                if summary:
                    avg_budget = summary[0]  # Extract AVG(budget)
                    sum_budget = summary[1]  # Extract SUM(budget)
   
    return render(request, "govmonitor/show_loc_infra.html", {
        "form": form,
        "records": records,
        "avg_budget": avg_budget,
        "sum_budget": sum_budget,
        "userid":userid,
        "password":password
    })


def agriculture_data(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT crop_type, SUM(area_acres) FROM land_records GROUP BY crop_type")
        results = cursor.fetchall()
    return render(request, 'govmonitor/agriculture_data.html', {'land_records':results, "user_id":user_id, "password":password})

def show_income_agri(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = AgriIncome()
    records = None
    avg_income = None
    total_income = None

    if request.method == 'POST':
        form = AgriIncome(request.POST)
        if form.is_valid():
            crop_type = form.cleaned_data['crop_type']

            with connection.cursor() as cursor:
                cursor.execute("SELECT name, income FROM citizen JOIN land_records ON land_records.citizen_id = citizen.citizen_id WHERE crop_type = %s;", [crop_type])
                records = cursor.fetchall()

                cursor.execute("SELECT AVG(income), SUM(income) FROM citizen JOIN land_records ON land_records.citizen_id = citizen.citizen_id WHERE crop_type = %s;", [crop_type])
                summary = cursor.fetchone()

                if summary:
                    avg_income = summary[0]  # Extract AVG(budget)
                    total_income = summary[1]  # Extract SUM(budget)

    return render(request, "govmonitor/show_income_agri.html", {
        "form": form,
        "records": records,
        "avg_income": avg_income,
        "total_income": total_income,
        "userid":userid,
        "password":password
    })

def show_edu_agri(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = AgriIncome()
    records = []

    if request.method == 'POST':
        form = AgriIncome(request.POST)
        if form.is_valid():
            crop_type = form.cleaned_data['crop_type']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT educational_qualification, COUNT(*)
                    FROM citizen
                    JOIN land_records ON land_records.citizen_id = citizen.citizen_id
                    WHERE land_records.crop_type = %s
                    GROUP BY educational_qualification;
                """, [crop_type])
               
                records = cursor.fetchall()

    return render(request, "govmonitor/show_edu_agri.html", {
        "form": form,
        "records": records,
        "userid": userid,
        "password": password
    })

def show_area_agri(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = AgriArea()
    records = []

    if request.method == 'POST':
        form = AgriArea(request.POST)
        if form.is_valid():
            area = form.cleaned_data['area']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name, SUM(area_acres) AS s 
                    FROM citizen 
                    JOIN land_records ON citizen.citizen_id = land_records.citizen_id 
                    GROUP BY name
                    HAVING SUM(area_acres) > %s;

                """, [area])
               
                records = cursor.fetchall()

    return render(request, "govmonitor/show_area_agri.html", {
        "form": form,
        "records": records,
        "userid":userid,
        "password":password
    })


def login_page(request):
    # if(request.user.is_anonymous):
    #     return redirect("/api/login_page")
    return render(request, 'general/login_page.html')

def census_data_login(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    return render(request, 'govmonitor/census_data_login.html')

def environment_data_login(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    return render(request, 'environment_data_login.html')

def agriculture_data_login(request):
    # if(request.user.is_anonymous):
    #     return redirect("/api/login_page")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT crop_type, SUM(area_acres) FROM land_records GROUP BY crop_type")
        results = cursor.fetchall()
    return render(request, 'general/agriculture_data_login.html', {'land_records':results})

def government_monitor(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    return render(request, 'govmonitor/government_monitor.html')

def show_general_census(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    today = date.today()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM census_data WHERE event_type = 'Birth' AND EXTRACT(YEAR FROM event_date)=%s;
        """, [today.year])
        result1 = cursor.fetchone()  # Fetch a single row

        cursor.execute("""
            SELECT COUNT(*)
            FROM census_data WHERE event_type = 'Death' AND EXTRACT(YEAR FROM event_date)=%s;
        """, [today.year])
        result2 = cursor.fetchone()  # Fetch a single row

    # Check if result is None (in case the table is empty)
    if result1 is None or all(v is None for v in result1):
        return render(request, "govmonitor/show_general_census.html", {"error": "No data available"})
   
    if result2 is None or all(v is None for v in result1):
        return render(request, "govmonitor/show_general_census.html", {"error": "No data available"})

    # Convert the tuple to a dictionary
    data = {
        "births": result1[0],
        "deaths": result2[0],
    }

    return render(request, "govmonitor/show_general_census.html", {"data": data, "user_id":user_id, "password":password})

def census_data_func(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = CensusDateForm()
    records = None

    if request.method == 'POST':
        form = CensusDateForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']

            with connection.cursor() as cursor:
                cursor.execute("SELECT name, event_type, event_date FROM census_data JOIN citizen ON citizen.citizen_id = census_data.citizen_id WHERE EXTRACT(YEAR FROM event_date) = %s AND EXTRACT(MONTH FROM event_date) = %s;", [year, month])
                records = cursor.fetchall()

    return render(request, "govmonitor/census_data.html", {"form":form, "records": records, "userid":userid, "password":password})

def census_date_count(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = CensusYearForm()
    records = None

    if request.method == 'POST':
        form = CensusYearForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        (SELECT COUNT(*) FROM census_data WHERE event_date BETWEEN %s AND %s AND event_type = 'Birth') AS total_births,
                        (SELECT COUNT(*) FROM census_data WHERE event_date BETWEEN %s AND %s AND event_type = 'Death') AS total_deaths,
                        (SELECT COUNT(*) FROM census_data
                         JOIN citizen ON census_data.citizen_id = citizen.citizen_id
                         WHERE event_date BETWEEN %s AND %s AND event_type = 'Birth' AND gender = 'Male') AS male_births,
                        (SELECT COUNT(*) FROM census_data
                         JOIN citizen ON census_data.citizen_id = citizen.citizen_id
                         WHERE event_date BETWEEN %s AND %s AND event_type = 'Birth' AND gender = 'Female') AS female_births;
                """, [start_date, end_date] * 4)
               
                records = cursor.fetchone()  # Fetch as a tuple

    return render(request, "govmonitor/census_date_count.html", {"form": form, "records": records, "userid":userid, "password":password})

def census_pop_count(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = CensusPopForm()
    records = None

    if request.method == 'POST':
        form = CensusPopForm(request.POST)
        if form.is_valid():
            event_date = form.cleaned_data['date_pop']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        COUNT(*) FILTER (
                            WHERE citizen.citizen_id NOT IN (
                                SELECT citizen_id FROM census_data
                                WHERE event_type = 'Death' AND event_date < %s
                            )
                            AND citizen.citizen_id IN (
                                SELECT citizen_id FROM census_data
                                WHERE event_type = 'Birth' AND event_date <= %s
                            )
                        ) AS total_population,
                       
                        COUNT(*) FILTER (
                            WHERE citizen.gender = 'Male'
                            AND citizen.citizen_id NOT IN (
                                SELECT citizen_id FROM census_data
                                WHERE event_type = 'Death' AND event_date < %s
                            )
                            AND citizen.citizen_id IN (
                                SELECT citizen_id FROM census_data
                                WHERE event_type = 'Birth' AND event_date <= %s
                            )
                        ) AS male_count,
                       
                        COUNT(*) FILTER (
                            WHERE citizen.gender = 'Female'
                            AND citizen.citizen_id NOT IN (
                                SELECT citizen_id FROM census_data
                                WHERE event_type = 'Death' AND event_date < %s
                            )
                            AND citizen.citizen_id IN (
                                SELECT citizen_id FROM census_data
                                WHERE event_type = 'Birth' AND event_date <= %s
                            )
                        ) AS female_count
                    FROM citizen
                    JOIN census_data ON citizen.citizen_id = census_data.citizen_id;
                """, [event_date] * 6)

                records = cursor.fetchone()

    return render(request, "govmonitor/census_pop_count.html", {"form": form, "records": records, "userid":userid, "password":password})

def census_edu_count(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = CensusPopForm()
    records = None

    if request.method == 'POST':
        form = CensusPopForm(request.POST)
        if form.is_valid():
            event_date = form.cleaned_data['date_pop']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        citizen.educational_qualification,
                        COUNT(DISTINCT citizen.citizen_id)
                    FROM citizen
                    JOIN census_data ON citizen.citizen_id = census_data.citizen_id
                    WHERE citizen.citizen_id NOT IN (
                        SELECT citizen_id FROM census_data
                        WHERE event_type = 'Death' AND event_date < %s
                    )
                    AND citizen.citizen_id IN (
                        SELECT citizen_id FROM census_data
                        WHERE event_type = 'Birth' AND event_date <= %s
                    )
                    GROUP BY citizen.educational_qualification;
                """, [event_date] * 2)

                records = cursor.fetchall()

    return render(request, "govmonitor/census_edu_count.html", {"form": form, "records": records, "userid":userid, "password":password})

def census_vacc_count(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = CensusPopForm()
    records = None

    if request.method == 'POST':
        form = CensusPopForm(request.POST)
        if form.is_valid():
            event_date = form.cleaned_data['date_pop']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        vaccinations.vaccine_type,
                        COUNT(DISTINCT citizen.citizen_id)
                    FROM citizen
                    JOIN census_data ON citizen.citizen_id = census_data.citizen_id
                    JOIN vaccinations ON citizen.citizen_id = vaccinations.citizen_id
                    WHERE citizen.citizen_id NOT IN (
                        SELECT citizen_id FROM census_data
                        WHERE event_type = 'Death' AND event_date < %s
                    )
                    AND citizen.citizen_id IN (
                        SELECT citizen_id FROM census_data
                        WHERE event_type = 'Birth' AND event_date <= %s
                    )
                    GROUP BY vaccinations.vaccine_type;
                """, [event_date] * 2)

                records = cursor.fetchall()

    return render(request, "govmonitor/census_vacc_count.html", {"form": form, "records": records, "userid":userid, "password":password})

def census_income_count(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    userid = request.GET.get('userid')
    password = request.GET.get('password')

    form = CensusPopForm()
    records = None

    if request.method == 'POST':
        form = CensusPopForm(request.POST)
        if form.is_valid():
            event_date = form.cleaned_data['date_pop']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        COALESCE(AVG(citizen.income), 0) AS avg_income,
                        COUNT(DISTINCT tax.payer_id) AS pending_tax_count,
                        COALESCE(AVG(tax.amount), 0) AS avg_pending_tax_amount
                    FROM citizen
                    LEFT JOIN tax ON citizen.citizen_id = tax.payer_id
                        AND tax.paid_status = 'DUE'
                        AND tax.due_date <= %s
                    WHERE citizen.citizen_id NOT IN (
                        SELECT citizen_id FROM census_data
                        WHERE event_type = 'Death' AND event_date < %s
                    )
                    AND citizen.citizen_id IN (
                        SELECT citizen_id FROM census_data
                        WHERE event_type = 'Birth' AND event_date <= %s
                    );
                """, [event_date] * 3)

                records = cursor.fetchone()

    return render(request, "govmonitor/census_income_count.html", {"form": form, "records": records, "userid":userid, "password":password})


def login_view(request):
    print(f"Request Method: {request.method}")  # Check if POST or GET
    print(f"GET Data: {request.GET}")  # Print GET request data
    print(f"POST Data: {request.POST}")  # Print POST request data
    if request.user.is_authenticated:
        userid = request.user.username  # Get logged-in user's ID
        print(userid)
    
        try:
            with connection.cursor() as cursor:
                # Fetch role from users table
                query = "SELECT role FROM users WHERE user_id = %s;"
                cursor.execute(query, [userid])
                role_row = cursor.fetchone()

                print(userid)

                if role_row is None:
                    return HttpResponse("User role not found.")

                role = role_row[0]  # Extract role name (e.g., "CITIZEN")

                if role == "CITIZEN":
                    # Fetch citizen details
                    citi = citizen.objects.raw('SELECT * from citizen where citizen_id = %s', [userid])[0]
                    
                    return render(request, "citizen/citizenhome.html", {"citizen": citi})

                elif role == "MONITOR":
                    # Fetch monitor details
                    query = "SELECT * FROM users WHERE user_id = %s;"
                    cursor.execute(query, [userid])
                    columns = [col[0] for col in cursor.description]
                    monitor_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

                    return render(request, "govmonitor/government_monitor.html", {"data": monitor_data})
                elif role == "EMPLOYEE":
                    emp = panchayat_employees.objects.raw("select * from panchayat_employees where employee_id = %s", [userid])[0]
                    return render(request, 'employee/emphome.html', {'emp':emp})
                elif role == "ADMIN":
                    return render(request, 'admin/admhome.html')
                else:
                    return HttpResponse("Access denied for this role.")

        except Exception as e:
            return HttpResponse(f"Error fetching role data: {e}")

    
    if request.method == "POST":
        print('hello')
        userid = request.POST.get("userid")
        role = request.POST.get("role")
        password = request.POST.get("password")
        user = authenticate(username = userid, password = password)
    if user is None:
        print("user not fetched\n")
        return redirect("/api/login_page")
    else:
        login(request, user)
        if not userid or not role or not password:
            return HttpResponse("All fields are required.")
        
        
        role_mapping = {"ADMIN": 1, "EMPLOYEE": 2, "CITIZEN": 3, "MONITOR": 4}
        role_id = role_mapping.get(role)
        print(role_id)
        
        if role_id is None:
            return HttpResponse("Invalid role.")
        
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM users WHERE user_id = %s AND password_user = %s AND role = %s;
                """
                cursor.execute(query, [userid, password, role])
                user = cursor.fetchone()
                
                if user:
                    if role_id == 3:
                        citi = citizen.objects.raw('SELECT * from citizen where citizen_id = %s', [userid])[0]
                        return render(request, "citizen/citizenhome.html", {"citizen": citi})
                    elif role_id == 4:
                        query = """
                        SELECT * FROM users WHERE user_id = %s;
                        """
                        cursor.execute(query, [userid])
                        columns = [col[0] for col in cursor.description]
                        monitor_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        return render(request, "govmonitor/government_monitor.html", {"data": monitor_data})
                    elif role_id == 2:
                        emp = panchayat_employees.objects.raw("select * from panchayat_employees where employee_id = %s", [userid])[0]
                        return render(request, 'employee/emphome.html', {'emp':emp})
                    elif role_id == 1:
                        return render(request, 'admin/admhome.html')
                    else:
                        return HttpResponse("Access denied for this role.")
                else:
                    return HttpResponse("Invalid credentials.")
        except Exception as e:
            return HttpResponse(f"Error during login: {e}")
    if(request.method == "GET"):
        userid = request.GET.get("userid")
        role = request.GET.get("role")
        password = request.GET.get("password")
        user = authenticate(username = userid, password = password)
    if user is None:
            return redirect("/api/login_page")
    else:
        login(request, user)
        if not userid or not role or not password:
            return HttpResponse("All fields are required.")
        
        role_mapping = {"ADMIN": 1, "EMPLOYEE": 2, "CITIZEN": 3, "MONITOR": 4}
        role_id = role_mapping.get(role)
        
        if role_id is None:
            return HttpResponse("Invalid role.")
        
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM users WHERE user_id = %s AND password_user = %s AND role = %s;
                """
                cursor.execute(query, [userid, password, role])
                user = cursor.fetchone()
                
                if user:
                    if role_id == 3:
                        citi = citizen.objects.raw('SELECT * from citizen where citizen_id = %s', [userid])[0]
                        return render(request, "citizen/citizenhome.html", {"citizen": citi})
                    elif role_id == 4:
                        query = """
                        SELECT * FROM users WHERE user_id = %s;
                        """
                        cursor.execute(query, [userid])
                        columns = [col[0] for col in cursor.description]
                        monitor_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        return render(request, "govmonitor/government_monitor.html", {"data": monitor_data})
                    elif role_id == 2:
                        emp = panchayat_employees.objects.raw("select * from panchayat_employees where employee_id = %s", [userid])[0]
                        return render(request, 'employee/emphome.html', {'emp':emp})
                    elif role_id == 1:
                        return render(request, 'admin/admhome.html')
                    else:
                        return HttpResponse("Access denied for this role.")
                else:
                    return HttpResponse("Invalid credentials.")
        except Exception as e:
            return HttpResponse(f"Error during login: {e}")
        

def infrastructure_data_monitor(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    if request.method == "POST":
        year = request.POST.get("year")
        location = request.POST.get("location")
       
        if not year or not location:
            return HttpResponse("Year and Location are required.")
       
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM assets
                WHERE EXTRACT(YEAR FROM installation_date) = %s
                AND location = %s;
                """
                cursor.execute(query, [year, location])
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
           
            return render(request, "infrastructure_data_monitor.html", {"data": data})
        except Exception as e:
            return HttpResponse(f"Error fetching data: {e}")
   
    return HttpResponse("Invalid request method.")


def infra_gen(request):
    # if(request.user.is_anonymous):
    #     return redirect("/api/login_page")
    with connection.cursor() as cursor:
        query = """
        SELECT type, location, COUNT(*) as count, SUM(budget) as total_budget
        FROM assets
        GROUP BY type, location
        """
        cursor.execute(query)
        results = cursor.fetchall()
   
    return render(request, 'general/infra_gen.html', {'asset_records': results})


def env_data_monitor(request):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    if request.method == "POST":
        year = request.POST.get("year")
        month = request.POST.get("month")
       
        if not year or not month:
            return HttpResponse("Year and Month are required.")
       
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM env_data
                WHERE EXTRACT(YEAR FROM date_of_record) = %s
                AND EXTRACT(MONTH FROM date_of_record) = %s;
                """
                cursor.execute(query, [year, month])
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
           
            return render(request, "env_data.html", {"data": data})
        except Exception as e:
            return HttpResponse(f"Error fetching data: {e}")

    return HttpResponse("Invalid request method.")

def members(request, household_id):
    if(request.user.is_anonymous):
        return redirect("/api/login_page")
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT * FROM citizen WHERE household_id = %s;
            """
            cursor.execute(query, [household_id])
            columns = [col[0] for col in cursor.description]
            members = [dict(zip(columns, row)) for row in cursor.fetchall()]
       
        return render(request, "members.html", {"members": members})
    except Exception as e:
        return HttpResponse(f"Error fetching household details: {e}")

def logout_view(request):
    request.session.flush() 
    logout(request)
    return redirect("/api/login_page")
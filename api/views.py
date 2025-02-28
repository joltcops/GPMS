from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import citizenSerializer, householdSerializer, welfare_schemesSerializer, land_recordsSerializer, assetsSerializer, vaccinationsSerializer, scheme_enrollmentsSerializer, census_dataSerializer, usersSerializer, panchayat_employeesSerializer
from .models import citizen, household, welfare_schemes, land_records, assets, vaccinations, scheme_enrollments, census_data, users, panchayat_employees, benefit_application, certificate, certificate_application
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection
from .forms import CitizenForm, BenefitForm, EnvDateForm, EnvValueForm, InfraDateForm, InfraLocForm, AgriIncome, AgriArea, CertificateForm, CensusDateForm, CensusYearForm, CensusPopForm, SchemeDateForm, SchemeNameForm
from datetime import date
from django.http import HttpResponse

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


@api_view(['GET'])
def getRoutes(request):
    routes=[
        '/token',
        '/token/refresh',
    ]
    return Response(routes)

#Get all books
@api_view(['GET'])
def getcitizens(request):
    citizens=citizen.objects.all()
    CitizenSerializer=citizenSerializer(citizens, many=True)
    return Response(CitizenSerializer.data)

def getschemes(request):
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    schemes=welfare_schemes.objects.all()
    return render(request, 'schemes.html', {'schemes': schemes, "user_id":user_id, "password":password})

def getschemes_gen(request):
    schemes=welfare_schemes.objects.all()
    return render(request, 'schemes_gen.html', {'schemes': schemes})

def show_date_scheme(request):
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

    return render(request, "show_date_scheme.html", {"form":form, "records":records})

def show_stat_scheme(request):
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

    return render(request, "show_stat_scheme.html", {"form":form, "records":records, "edu":edu})

@api_view(['POST'])
def addcitizen(request):
    data=request.data
    CitizenSerializer=citizenSerializer(data=data)
    if CitizenSerializer.is_valid():       
        CitizenSerializer.save()
    return Response(CitizenSerializer.data)

@api_view(["GET"])
def get_citizens(request, fields):
    allowed_fields = {"name", "educational_qualification", "age", "gender"}  # Allowed columns
    requested_fields = fields.split(",")  # Convert comma-separated string to a list
    invalid_fields = set(requested_fields) - allowed_fields  # Check for invalid fields

    if invalid_fields:
        return Response({"error": f"Invalid fields: {', '.join(invalid_fields)}"}, status=400)

    fields_query = ", ".join(requested_fields)  # Convert list back to SQL-safe string

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {fields_query} FROM citizen")  # Query only required fields
        results = cursor.fetchall()

    data = [dict(zip(requested_fields, row)) for row in results]  # Convert result to JSON format
    return Response(data)  # DRF handles the response


def generate_new_application_id():
    last_application = benefit_application.objects.order_by('-application_id').first()
    
    if last_application:
        last_id = last_application.application_id  # Example: 'BR005'
        last_num = int(last_id[3:])  # Extract numeric part -> 5
        new_id = f"BR00{last_num + 1}"  # Increment and format -> 'BR006'
    else:
        new_id = "BR001"  # If no records exist, start from 'BR001'

    return new_id

def generate_new_certificate_id():
    last_application = certificate_application.objects.order_by('-application_id').first()
    
    if last_application:
        last_id = last_application.application_id  # Example: 'BR005'
        last_num = int(last_id[3:])  # Extract numeric part -> 5
        new_id = f"AP00{last_num + 1}"  # Increment and format -> 'BR006'
    else:
        new_id = "AP001"  # If no records exist, start from 'BR001'

    return new_id

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
                parent=parent_inst
            )
            print("Form is valid")
            print(form.cleaned_data)
            citi.save()
            return redirect('')  # Replace with your success page URL
    else:
        form = CitizenForm()
    return render(request, 'addcitizen.html', {'form': form})

def add_benefit_application(request):
    if request.method == 'POST':
        form = BenefitForm(request.POST)
        if form.is_valid():
            application_id = generate_new_application_id()
            scheme_id = form.cleaned_data['scheme_id']
            citizen_id = form.cleaned_data['citizen_id']

            scheme_id_inst = welfare_schemes.objects.get(scheme_id=scheme_id)

            # Replace citizen.objects.get(...) with raw SQL query
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM citizen WHERE citizen_id = %s;", [citizen_id])
                row = cursor.fetchone()

            if row is None:
                print("Citizen not found")
                return render(request, 'apply_benefit.html', {'form': form, 'error': 'Citizen not found'})

            citizen_id_inst = row[0]  # Extract the citizen_id

            new_app = benefit_application(
                application_id=application_id,
                citizen_id_id=citizen_id_inst,  # Use `_id` suffix for ForeignKey
                scheme_id=scheme_id_inst,
                status='PENDING'
            )

            print("Form is valid")
            print(form.cleaned_data)
            new_app.save()
            return redirect('/api')
    else:
        form = BenefitForm()
    return render(request, 'apply_benefit.html', {'form': form})

def approve_certificate(request, application_id, employee_id):
    # Get application or return 404 if not found
    application = get_object_or_404(certificate_application, application_id=application_id)

    if application:
        # Update application status
        application.status = 'APPROVED'
        application.save()

        # Fetch related objects
        applicant = get_object_or_404(citizen, citizen_id=application.applicant_id)
        official = get_object_or_404(panchayat_employees, employee_id=employee_id)

        # Create and save the certificate
        new_cert = certificate(
            certificate_type=application.certificate_type,
            applicant_id=applicant,
            issue_date=date.today(),
            issuing_official=official
        )
        new_cert.save()

        return redirect('')  # Replace with the correct URL name
    else:
        return render(request, 'approve_certificate.html', {'application': application})

def home_page(request):
    return render(request, 'index.html')

def citizen_list(request):
    citizens = citizen.objects.all()
    return render(request, 'citizen_list.html', {'citizens': citizens})

def citizen_detail(request, citizen_id):
    citi = get_object_or_404(citizen, citizen_id=citizen_id)
    return render(request, 'citizen_detail.html', {'citizen': citi})

def panchayat_details(request):
    employee = panchayat_employees.objects.all()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT name, role, department FROM citizen, panchayat_employees WHERE citizen.citizen_id=panchayat_employees.citizen_id")  # Query only required fields
        results = cursor.fetchall()
    #data = [dict(zip(row)) for row in results] 
    return render(request, 'panchayat_details.html', {'employee': results})

def environment_data(request):
    return render(request, 'environment_data.html')

# def infrastructure_data(request):
#     return render(request, 'infrastructure_data.html')

# def login_page(request):
#     return render(request, 'login_page.html')

def show_general_env(request):
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
        return render(request, "general_env_1.html", {"error": "No data available", "user_id": user_id, "password": password})

    # Convert the tuple to a dictionary
    data = {
        "avg_rainfall": result[0],
        "avg_aqi": result[1],
        "avg_gwl": result[2],
        "avg_temperature": result[3],
        "avg_humidity": result[4],
        "avg_wind_speed": result[5]
    }

    return render(request, "general_env.html", {"data": data, "user_id": user_id, "password": password})


def show_general_env_1(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT AVG(rainfall), AVG(aqi), AVG(gwl), AVG(temperature), 
                   AVG(humidity), AVG(wind_speed) 
            FROM env_data;
        """)
        result = cursor.fetchone()  # Fetch a single row

    # Check if result is None (in case the table is empty)
    if result is None or all(v is None for v in result):
        return render(request, "general_env_1.html", {"error": "No data available"})

    # Convert the tuple to a dictionary
    data = {
        "avg_rainfall": result[0],
        "avg_aqi": result[1],
        "avg_gwl": result[2],
        "avg_temperature": result[3],
        "avg_humidity": result[4],
        "avg_wind_speed": result[5]
    }

    return render(request, "general_env_1.html", {"data": data})


def show_date_env(request):
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

    return render(request, "show_date_env.html", {"form": form, "records": records})

def show_val_env(request):
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

    return render(request, "show_val_env.html", {"form": form, "records": records})

def show_above_avg_env(request):
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

    return render(request, "show_above_avg_env.html", {"parameters": parameters, "selected_param": selected_param, "records": records})



# def panchayat_details(request):
#     employee = panchayat_employees.objects.all()
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT name, role, department FROM citizen, panchayat_employees WHERE citizen.citizen_id=panchayat_employees.citizen_id")  # Query only required fields
#         results = cursor.fetchall()
#     #data = [dict(zip(row)) for row in results] 
#     return render(request, 'panchayat_details.html', {'employee': results})

def environment_data(request):

    return render(request, 'environment_data.html')

def infrastructure_data(request):
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT SUM(budget), AVG(budget), MAX(budget), MIN(budget) FROM assets;")
        results = cursor.fetchall()
    return render(request, 'infrastructure_data.html', {'asset_records':results, "user_id":user_id, "password":password})

def show_date_infra(request):
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
                
    return render(request, "show_date_infra.html", {
        "form": form, 
        "records": records,
        "avg_budget": avg_budget,
        "sum_budget": sum_budget
    })

def show_loc_infra(request):
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
    
    return render(request, "show_loc_infra.html", {
        "form": form, 
        "records": records,
        "avg_budget": avg_budget,
        "sum_budget": sum_budget
    })


def agriculture_data(request):
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT crop_type, SUM(area_acres) FROM land_records GROUP BY crop_type")
        results = cursor.fetchall()
    return render(request, 'agriculture_data.html', {'land_records':results, "user_id":user_id, "password":password})

def show_income_agri(request):
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

    return render(request, "show_income_agri.html", {
        "form": form, 
        "records": records,
        "avg_income": avg_income,
        "total_income": total_income
    })

def show_edu_agri(request):
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

    return render(request, "show_edu_agri.html", {
        "form": form, 
        "records": records,
    })

def show_area_agri(request):
    form = AgriArea()
    records = []

    if request.method == 'POST':
        form = AgriArea(request.POST)
        if form.is_valid():
            area = form.cleaned_data['area']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name, area_acres FROM citizen JOIN land_records ON citizen.citizen_id = land_records.citizen_id WHERE area_acres>%s;
                """, [area])
                
                records = cursor.fetchall()

    return render(request, "show_area_agri.html", {
        "form": form, 
        "records": records,
    })


def login_page(request):
    return render(request, 'login_page.html')

def census_data_login(request):
    return render(request, 'census_data_login.html')

def environment_data_login(request):
    return render(request, 'environment_data_login.html')

def agriculture_data_login(request):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT crop_type, SUM(area_acres) FROM land_records GROUP BY crop_type")
        results = cursor.fetchall()
    return render(request, 'agriculture_data_login.html', {'land_records':results})

def infrastructure_data_login(request):
    return render(request, 'infrastructure_data_login.html')

def government_monitor(request):
    return render(request, 'government_monitor.html')

def show_general_census(request):
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
        return render(request, "show_general_census.html", {"error": "No data available"})
    
    if result2 is None or all(v is None for v in result1):
        return render(request, "show_general_census.html", {"error": "No data available"})

    # Convert the tuple to a dictionary
    data = {
        "births": result1[0],
        "deaths": result2[0],
    }

    return render(request, "show_general_census.html", {"data": data, "user_id":user_id, "password":password})

def census_data_func(request):
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

    return render(request, "census_data.html", {"form":form, "records": records})

def census_date_count(request):
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

    return render(request, "census_date_count.html", {"form": form, "records": records})

def census_pop_count(request):
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

    return render(request, "census_pop_count.html", {"form": form, "records": records})

def census_edu_count(request):
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

    return render(request, "census_edu_count.html", {"form": form, "records": records})

def census_vacc_count(request):
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

    return render(request, "census_vacc_count.html", {"form": form, "records": records})

def census_income_count(request):
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

    return render(request, "census_income_count.html", {"form": form, "records": records})


def login_view(request):
    print(f"Request Method: {request.method}")  # Check if POST or GET
    print(f"GET Data: {request.GET}")  # Print GET request data
    print(f"POST Data: {request.POST}")  # Print POST request data
    if request.method == "POST":
        print('hello')
        userid = request.POST.get("userid")
        role = request.POST.get("role")
        password = request.POST.get("password")
        
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
                        query = """
                        SELECT * FROM citizen,users WHERE user_id = %s and citizen.citizen_id = users.user_id;
                        """
                        cursor.execute(query, [userid])
                        columns = [col[0] for col in cursor.description]
                        citizen_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        return render(request, "citizen_detail.html", {"data": citizen_data})
                    elif role_id == 4:
                        query = """
                        SELECT * FROM users WHERE user_id = %s;
                        """
                        cursor.execute(query, [userid])
                        columns = [col[0] for col in cursor.description]
                        monitor_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        return render(request, "government_monitor.html", {"data": monitor_data})
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
                        query = """
                        SELECT * FROM citizen,users WHERE user_id = %s and citizen.citizen_id = users.user_id;
                        """
                        cursor.execute(query, [userid])
                        columns = [col[0] for col in cursor.description]
                        citizen_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        return render(request, "citizen_detail.html", {"data": citizen_data})
                    elif role_id == 4:
                        query = """
                        SELECT * FROM users WHERE user_id = %s;
                        """
                        cursor.execute(query, [userid])
                        columns = [col[0] for col in cursor.description]
                        monitor_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        return render(request, "government_monitor.html", {"data": monitor_data})
                    else:
                        return HttpResponse("Access denied for this role.")
                else:
                    return HttpResponse("Invalid credentials.")
        except Exception as e:
            return HttpResponse(f"Error during login: {e}")
        
def login_view_1(request):
    if request.method == "POST":
        citizen_id = request.POST.get("citizen_id")
        
        # if not citizen_id:  # Handle missing citizen_id
        #     return render(request, "error.html", {"message": "Citizen ID is required."})

        with connection.cursor() as cursor:  # Get DB cursor safely
            query = """
                        SELECT * FROM citizen,users WHERE user_id = %s and citizen.citizen_id = users.user_id;
                        """
            cursor.execute(query, [citizen_id])
            columns = [col[0] for col in cursor.description]
            citizen_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return render(request, "citizen_detail.html", {"data": citizen_data})

    # return render(request, "login.html")  # Handle GET request
 
def infrastructure_data_monitor(request):
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
    with connection.cursor() as cursor:
        query = """
        SELECT type, location, COUNT(*) as count, SUM(budget) as total_budget
        FROM assets
        GROUP BY type, location
        """
        cursor.execute(query)
        results = cursor.fetchall()
    
    return render(request, 'infra_gen.html', {'asset_records': results})


def env_data_monitor(request):
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
    
def certificates(request, citizen_id):
    return render(request, 'certificates.html', {"citizen_id": citizen_id})
    
def apply_certificate(request):
    citizen_id = request.GET.get("citizen_id")  # Fetch from GET request

    if request.method == 'POST':
        form = CertificateForm(request.POST)

        if form.is_valid():
            application_id = generate_new_certificate_id()
            applicant_id = form.cleaned_data['applicant_id']  # Get applicant_id from form
            certificate_type = form.cleaned_data['certificate_type']

            # Query citizen using raw SQL
            with connection.cursor() as cursor:
                cursor.execute("SELECT citizen_id FROM citizen WHERE citizen_id = %s;", [citizen_id])
                row = cursor.fetchone()

                cursor.execute("SELECT user_id, role, password_user FROM users JOIN citizen ON citizen.citizen_id = users.user_id WHERE citizen.citizen_id = %s", [citizen_id])
                user_entry = cursor.fetchone()

            if row is None:
                print("Citizen not found")
                return render(request, 'apply_certificate.html', {'form': form, 'error': 'Citizen not found'})

            citizen_id_inst = row[0]  # Extract the citizen_id

            # **Check if applicant_id matches citizen_id**
            if str(applicant_id) != str(citizen_id_inst):  
                return render(request, 'apply_certificate.html', {'form': form, 'error': 'Applicant ID does not match Citizen ID.'})

            # Check if certificate has already been applied
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM certificate_application WHERE citizen_id = %s AND certificate_type = %s;",
                    [citizen_id, certificate_type]
                )
                cert_exists = cursor.fetchone()[0]  # Get count

            if cert_exists > 0:
                return render(request, 'apply_certificate.html', {'form': form, 'error': 'Certificate already applied for.'})

            # Extract password from users table
            with connection.cursor() as cursor:
                cursor.execute("SELECT password_user FROM users WHERE user_id = %s;", [citizen_id])
                user_row = cursor.fetchone()

            if user_row is None:
                print("User not found in users table")
                return render(request, 'apply_certificate.html', {'form': form, 'error': 'User not found'})

            password = user_row[0]  # Extract password from the database

            # Insert new certificate application
            new_app = certificate_application(
                application_id=application_id,
                certificate_type=certificate_type,
                citizen_id_id=citizen_id_inst,
                status='PENDING'
            )

            print("Form is valid")
            print(form.cleaned_data)
            new_app.save()

            # Redirect to login_view with userid (citizen_id), role as CITIZEN, and extracted password
            return redirect(f'/api/login_view?userid={citizen_id_inst}&role=CITIZEN&password={password}')
    
    else:
        form = CertificateForm()
    
    return render(request, 'apply_certificate.html', {'form': form})

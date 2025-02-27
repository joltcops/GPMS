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
from .forms import CitizenForm, BenefitForm, EnvDateForm, EnvValueForm
from datetime import date
from django.http import HttpResponse


count_benefit=3

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
    schemes=welfare_schemes.objects.all()
    return render(request, 'schemes.html', {'schemes': schemes})

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
                cursor.execute("SELECT citizen_id FROM citizen WHERE citizen_id = %s", [citizen_id])
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
            return redirect('')
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

# def agriculture_data(request):
#     return render(request, 'agriculture_data.html')

# def login_page(request):
#     return render(request, 'login_page.html')

def show_general_env(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT AVG(rainfall), AVG(aqi), AVG(gwl), AVG(temperature), 
                   AVG(humidity), AVG(wind_speed) 
            FROM env_data;
        """)
        result = cursor.fetchone()  # Fetch a single row

    # Check if result is None (in case the table is empty)
    if result is None or all(v is None for v in result):
        return render(request, "show_general_env.html", {"error": "No data available"})

    # Convert the tuple to a dictionary
    data = {
        "avg_rainfall": result[0],
        "avg_aqi": result[1],
        "avg_gwl": result[2],
        "avg_temperature": result[3],
        "avg_humidity": result[4],
        "avg_wind_speed": result[5]
    }

    return render(request, "general_env.html", {"data": data})


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
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(type), SUM(budget), AVG(budget),type FROM assets GROUP BY type")
        results = cursor.fetchall()
    return render(request, 'infrastructure_data.html', {'asset_records':results})

def agriculture_data(request):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT crop_type, SUM(area_acres) FROM land_records GROUP BY crop_type")
        results = cursor.fetchall()
    return render(request, 'agriculture_data.html', {'land_records':results})


def login_page(request):
    return render(request, 'login_page.html')

def census_data_login(request):
    return render(request, 'census_data_login.html')

def environment_data_login(request):
    return render(request, 'environment_data_login.html')

def agriculture_data_login(request):
    return render(request, 'agriculture_data_login.html')

def infrastructure_data_login(request):
    return render(request, 'infrastructure_data_login.html')

def government_monitor(request):
    return render(request, 'government_monitor.html')

def census_data_func(request):
    if request.method == "POST":
        year = request.POST.get("year")
        month = request.POST.get("month")
        
        if not year or not month:
            return HttpResponse("Year and Month are required.")
        
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM census_data
                WHERE EXTRACT(YEAR FROM event_date) = %s
                AND EXTRACT(MONTH FROM event_date) = %s;
                """
                cursor.execute(query, [year, month])
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return render(request, "census_data.html", {"data": data})
        except Exception as e:
            return HttpResponse(f"Error fetching data: {e}")
    
    return HttpResponse("Invalid request method.")

def login_view(request):
    if request.method == "POST":
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
                        return render(request, "government_monitor.html")
                    else:
                        return HttpResponse("Access denied for this role.")
                else:
                    return HttpResponse("Invalid credentials.")
        except Exception as e:
            return HttpResponse(f"Error during login: {e}")
    
    return HttpResponse("Invalid request method.")

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
    if request.method == "POST":
        citizen_id = request.POST.get("citizen_id")
        certificate_type = request.POST.get("certificate_type")

        if not citizen_id or not certificate_type:
            return HttpResponse("Citizen ID and Certificate Type are required.")

        try:
            last_application = certificate_application.objects.order_by('-application_id').first()

            if last_application:
                last_id = int(last_application.application_id[4:])  # Extract numeric part
                new_id = f"CERT{last_id + 1}"
            else:
                new_id = "CERT001"  # Start numbering if no records exist

            certificate = certificate_application(
                application_id=new_id,
                certificate_type=certificate_type,
                status="PENDING",
                applicant_id=citizen_id
            )
            certificate.save()

            return HttpResponse("Certificate application submitted successfully.")
        except Exception as e:
            return HttpResponse(f"Error submitting application: {e}")

    return HttpResponse("Invalid request method.")


    
    















    


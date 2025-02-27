from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import citizenSerializer, householdSerializer, welfare_schemesSerializer, land_recordsSerializer, assetsSerializer, vaccinationsSerializer, scheme_enrollmentsSerializer, census_dataSerializer, usersSerializer, panchayat_employeesSerializer
from .models import citizen, household, welfare_schemes, land_records, assets, vaccinations, scheme_enrollments, census_data, users, panchayat_employees, certificate_application
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection
from .forms import CitizenForm
from django.http import HttpResponse

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


    
    















    


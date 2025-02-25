from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import citizenSerializer
from .models import citizen
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.http import JsonResponse
from django.db import connection

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

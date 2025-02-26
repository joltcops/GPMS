from rest_framework.serializers import ModelSerializer
from .models import household
from .models import citizen
from .models import welfare_schemes, land_records, assets, vaccinations, scheme_enrollments, census_data, users, panchayat_employees

class citizenSerializer(ModelSerializer):
    class Meta:
        model = citizen
        fields = '__all__' 

class householdSerializer(ModelSerializer):
    class Meta:
        model = household
        fields = '__all__'

class welfare_schemesSerializer(ModelSerializer):
    class Meta:
        model = welfare_schemes
        fields = '__all__'

class land_recordsSerializer(ModelSerializer):
    class Meta:
        model = land_records
        fields = '__all__'

class assetsSerializer(ModelSerializer):
    class Meta:
        model = assets
        fields = '__all__'

class vaccinationsSerializer(ModelSerializer):
    class Meta:
        model = vaccinations
        fields = '__all__'

class scheme_enrollmentsSerializer(ModelSerializer):
    class Meta:
        model = scheme_enrollments
        fields = '__all__'

class census_dataSerializer(ModelSerializer):
    class Meta:
        model = census_data
        fields = '__all__'

class usersSerializer(ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'

class panchayat_employeesSerializer(ModelSerializer):
    class Meta:
        model = panchayat_employees
        fields = '__all__'
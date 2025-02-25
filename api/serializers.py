from rest_framework.serializers import ModelSerializer
from .models import household
from .models import citizen

class citizenSerializer(ModelSerializer):
    class Meta:
        model = citizen
        fields = '__all__' 

class householdSerializer(ModelSerializer):
    class Meta:
        model = household
        fields = '__all__'
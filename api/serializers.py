from rest_framework.serializers import ModelSerializer
from .models import citizen

class citizenSerializer(ModelSerializer):
    class Meta:
        model = citizen
        fields = '__all__' 
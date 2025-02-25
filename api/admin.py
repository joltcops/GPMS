from django.contrib import admin
from .models import citizen
from .models import household

admin.site.register(household)
admin.site.register(citizen)  # Register the citizen model

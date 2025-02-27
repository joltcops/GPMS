from django.contrib import admin
from .models import citizen
from .models import household
from .models import land_records
from .models import assets
from .models import vaccinations
from .models import panchayat_employees
from .models import scheme_enrollments
from .models import welfare_schemes
from .models import census_data
from .models import certificate_application
from .models import certificate
from .models import tax
from .models import benefit_application
from .models import env_data

admin.site.register(household)
admin.site.register(citizen)
admin.site.register(land_records)
admin.site.register(assets)
admin.site.register(vaccinations)
admin.site.register(panchayat_employees)
admin.site.register(scheme_enrollments)
admin.site.register(welfare_schemes)
admin.site.register(census_data)
admin.site.register(certificate_application)
admin.site.register(certificate)
admin.site.register(tax)
admin.site.register(benefit_application)
admin.site.register(env_data)
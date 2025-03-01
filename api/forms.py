from django import forms
from .models import citizen, household

class CitizenForm(forms.Form):
    citizen_id = forms.CharField(max_length=511)
    name = forms.CharField(max_length=511)
    gender = forms.CharField(max_length=15)
    dob = forms.DateField()
    educational_qualification = forms.CharField(max_length=511)
    household = forms.CharField(max_length=511)
    parent = forms.CharField(max_length=511)
    income = forms.IntegerField()
    

class LandForm(forms.Form):
    land_id = forms.CharField(max_length=511)
    area_acres = forms.IntegerField()
    crop_type = forms.CharField(max_length=511)

class VaccineForm(forms.Form):
    vaccination_id = forms.CharField(max_length=511)
    vaccine_type = forms.CharField(max_length=511)
    date_administered = forms.DateField()

class AssetsForm(forms.Form):
    asset_id = forms.CharField(max_length=511)
    type = forms.CharField(max_length=511)
    location = forms.CharField(max_length=511)
    installation_date = forms.DateField()
    budget = forms.IntegerField()

class CensusForm(forms.Form):
    census_id = forms.CharField(max_length=511)
    household_id = forms.CharField(max_length=511)
    citizen_id = forms.CharField(max_length=511)
    event_type = forms.CharField(max_length=511)
    event_date = forms.DateField()

class WelfareForm(forms.Form):
    scheme_id = forms.CharField(max_length=511)
    name = forms.CharField(max_length=511)
    description = forms.CharField(max_length=511)

class EnvForm(forms.Form):
    record_id = forms.CharField(max_length=511)
    rainfall = forms.IntegerField()
    aqi = forms.IntegerField()
    gwl = forms.IntegerField()
    date_of_record = forms.DateField()
    temperature = forms.IntegerField()
    humidity = forms.IntegerField()
    wind_speed = forms.IntegerField()

class HouseForm(forms.Form):
    household_id = forms.CharField(max_length=511)
    address = forms.CharField(max_length=2047)
    category = forms.CharField(max_length=511)
    income = forms.IntegerField()

class TaxForm(forms.Form):
    tax_id = forms.CharField(max_length=511)
    type = forms.CharField(max_length=511)
    amount = forms.IntegerField()
    due_date = forms.DateField()
    paid_status = forms.CharField(max_length=511)

class BenefitForm(forms.Form):
    application_id = forms.CharField(max_length=511)
    scheme_id = forms.CharField(max_length=511)

class CertificateForm(forms.Form):
    application_id = forms.CharField(max_length=511)
    certificate_type = forms.CharField(max_length=511)

class CertificateApprovalForm(forms.Form):
    certificate_id = forms.CharField(max_length=511)
    issue_date = forms.DateField()
    issuing_official = forms.CharField(max_length=511)

class BenefitApprovalForm(forms.Form):
    enrollment_id = forms.CharField(max_length=511)
    enrollment_date = forms.DateField()

class EmployeeForm(forms.Form):
    employee_id = forms.CharField(max_length=511)
    citizen_id = forms.CharField(max_length=511)
    department = forms.CharField(max_length=511)
    role = forms.CharField(max_length=511)

class EnvDateForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

class EnvValueForm(forms.Form):
    temperature = forms.IntegerField()
    air_quality_index = forms.IntegerField()
    ground_water_level = forms.IntegerField()
    humidity = forms.IntegerField()
    rainfall = forms.IntegerField()

class InfraDateForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

class InfraLocForm(forms.Form):
    location = forms.CharField(max_length=511)
    type = forms.CharField(max_length=511)

class AgriIncome(forms.Form):
    crop_type = forms.CharField(max_length=511)

class AgriArea(forms.Form):
    area = forms.IntegerField()

class CensusDateForm(forms.Form):
    year = forms.IntegerField()
    month = forms.IntegerField()

class CensusYearForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

class CensusPopForm(forms.Form):
    date_pop = forms.DateField()

class SchemeDateForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

class SchemeNameForm(forms.Form):
    name = forms.CharField()

from django import forms

class CitizenForm(forms.Form):
    citizen_id = forms.CharField(max_length=511)
    name = forms.CharField(max_length=511)
    gender = forms.CharField(max_length=15)
    dob = forms.DateField()
    educational_qualification = forms.CharField(max_length=511)
    household = forms.CharField(max_length=511)
    parent = forms.CharField(max_length=511)

class BenefitForm(forms.Form):
    scheme_id = forms.CharField(max_length=511)
    applicant_id = forms.CharField(max_length=511)

class CertificateForm(forms.Form):
    certificate_type = forms.CharField(max_length=511)
    applicant_id = forms.CharField(max_length=511)

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
from django import forms

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
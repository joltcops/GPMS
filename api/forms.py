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
    citizen_id = forms.CharField(max_length=511)
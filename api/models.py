from django.db import models

class household(models.Model):
    household_id = models.CharField(max_length=511, primary_key=True)
    address = models.CharField(max_length=2047)
    income = models.IntegerField()

    class Meta:
        db_table = 'household'
        managed=True

    def __str__(self):
        return self.address


class citizen(models.Model):
    citizen_id = models.CharField(max_length=511, primary_key=True)
    name = models.CharField(max_length=511)
    gender = models.CharField(max_length=15)
    dob = models.DateField()
    educational_qualification = models.CharField(max_length=511)
    household = models.ForeignKey(household, on_delete=models.CASCADE, db_column='household_id')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='parent_id')

    class Meta:
        db_table = 'citizen'
        managed=True

    def __str__(self):
        return self.name


class land_records(models.Model):
    land_id = models.CharField(max_length=511, primary_key=True)  # Explicit primary key
    citizen_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    area_acres = models.IntegerField()
    crop_type = models.CharField(max_length=511)

    class Meta:
        db_table = 'land_records'
        managed = False

    def __str__(self):
        return self.land_id



class panchayat_employees(models.Model):
    employee_id = models.CharField(max_length=511, primary_key=True)
    citizen_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    role = models.CharField(max_length=511)

    class Meta:
        db_table = 'panchayat_employees'
        managed=True

    def __str__(self):
        return self.citizen.name


class assets(models.Model):
    asset_id = models.CharField(max_length=511, primary_key=True)
    type = models.CharField(max_length=511)
    location = models.CharField(max_length=2047)
    installation_date = models.DateField()

    class Meta:
        db_table = 'assets'
        managed=True

    def __str__(self):
        return self.type


class welfare_schemes(models.Model):
    scheme_id = models.CharField(max_length=511, primary_key=True)
    name = models.CharField(max_length=511)
    description = models.TextField()

    class Meta:
        db_table = 'welfare_schemes'
        managed=True

    def __str__(self):
        return self.name


class scheme_enrollments(models.Model):
    enrollment_id = models.CharField(max_length=511, primary_key=True)
    citizen_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    scheme_id = models.ForeignKey(welfare_schemes, on_delete=models.CASCADE, db_column='scheme_id')
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'scheme_enrollments'
        #unique_together = ('enrollment_id', 'citizen_id', 'scheme_id')
        managed=True

    def __str__(self):
        return self.citizen.name


class vaccinations(models.Model):
    vaccination_id = models.CharField(max_length=511, primary_key=True)
    citizen_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    vaccine_type = models.CharField(max_length=511)
    date_administered = models.DateField()

    class Meta:
        db_table = 'vaccinations'
        #unique_together = ('vaccination_id', 'citizen_id')
        managed=True

    def __str__(self):
        return self.vaccine_type


class census_data(models.Model):
    census_id = models.CharField(max_length=511, primary_key=True)
    household_id = models.ForeignKey(household, on_delete=models.CASCADE, db_column='household_id')
    citizen_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    event_type = models.CharField(max_length=511)
    event_date = models.DateField()

    class Meta:
        db_table = 'census_data'
        #unique_together = ('household_id', 'citizen_id', 'event_type')
        managed=True

    def __str__(self):
        return self.event_type
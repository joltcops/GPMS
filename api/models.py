from django.db import models

class users(models.Model):

    ADMIN = 1
    EMPLOYEE = 2
    CITIZEN = 3
    MONITOR = 4
    ROLES=(
        (ADMIN, 'ADMIN'),
        (EMPLOYEE, 'EMPLOYEE'),
        (CITIZEN, 'CITIZEN'),
        (MONITOR, 'MONITOR')
    )
    user_id = models.CharField(max_length=511, primary_key=True)
    role = models.CharField(max_length=511)
    password_user = models.CharField(max_length=511)
    

class household(models.Model):
    household_id = models.CharField(max_length=511, primary_key=True)
    address = models.CharField(max_length=2047)
    category = models.CharField(max_length=511)
    income = models.IntegerField()

    class Meta:
        db_table = 'household'
        managed=True

    def __str__(self):
        return self.address


class citizen(models.Model):
    citizen_id = models.ForeignKey(users, on_delete=models.CASCADE, db_column='user_id', primary_key=True)
    name = models.CharField(max_length=511)
    gender = models.CharField(max_length=15)
    dob = models.DateField()
    educational_qualification = models.CharField(max_length=511)
    household_id = models.ForeignKey(household, on_delete=models.CASCADE, db_column='household_id')
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='parent_id')
    income = models.IntegerField()

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
    employee_id = models.ForeignKey(users, on_delete=models.CASCADE, db_column='user_id', primary_key=True)
    citizen_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    role = models.CharField(max_length=511)
    department = models.CharField(max_length=511)

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
    budget=models.IntegerField()

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
    
class certificate_application(models.Model):
    INCOME_CERTIFICATE = 1
    CASTE_CERTIFICATE = 2
    LAND_OWNERSHIP_CERTIFICATE = 3
    BIRTH_CERTIFICATE = 4
    CERTIFICATES = (
        (INCOME_CERTIFICATE, 'INCOME CERTIFICATE'),
        (CASTE_CERTIFICATE, 'CASTE CERTIFICATE'),
        (LAND_OWNERSHIP_CERTIFICATE, 'LAND OWNERSHIP CERTIFICATE'),
        (BIRTH_CERTIFICATE, 'BIRTH CERTIFICATE')
    )
    PENDING = 5
    APPROVED = 6
    STATUS = (
        (PENDING, 'PENDING'),
        (APPROVED, 'APPROVED')
    )
    application_id = models.CharField(max_length=511, primary_key=True)
    certificate_type = models.CharField(max_length=511)
    status = models.CharField(max_length=511)
    applicant_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')

    class Meta:
        db_table = 'certificate_application'
        #unique_together = ('household_id', 'citizen_id', 'event_type')
        managed=True

    def __str__(self):
        return self.application_id

class certificate(models.Model):
    certificate_id = models.CharField(max_length=511, primary_key=True)
    certificate_type = models.CharField(max_length=511)
    applicant_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    issue_date = models.DateField()
    issuing_official = models.ForeignKey(panchayat_employees, on_delete=models.CASCADE, db_column='employee_id')

    class Meta:
        db_table = 'certificate'
        managed = True

    def __str__(self):
        return self.certificate_type

class tax(models.Model):
    TAX_TYPES = [
        ('PROPERTY', 'Property'),
        ('WATER', 'Water'),
    ]
    PAID_STATUS = [
        ('PAID', 'Paid'),
        ('DUE', 'Due'),
    ]
    
    tax_id = models.CharField(max_length=511, primary_key=True)
    payer_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    type = models.CharField(max_length=511, choices=TAX_TYPES)
    amount = models.IntegerField()
    due_date = models.DateField()
    paid_status = models.CharField(max_length=511, choices=PAID_STATUS)

    class Meta:
        db_table = 'tax'
        managed = True

    def __str__(self):
        return self.type

class benefit_application(models.Model):
    APPLICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
    ]
    
    application_id = models.CharField(max_length=511, primary_key=True)
    user_id = models.ForeignKey(citizen, on_delete=models.CASCADE, db_column='citizen_id')
    scheme_id = models.ForeignKey(welfare_schemes, on_delete=models.CASCADE, db_column='scheme_id')
    status = models.CharField(max_length=511, choices=APPLICATION_STATUS)

    class Meta:
        db_table = 'benefit_application'
        managed = True

    def __str__(self):
        return self.application_id

class env_data(models.Model):
    record_id = models.CharField(max_length=511, primary_key=True)
    rainfall = models.IntegerField()
    aqi = models.IntegerField()
    gwl = models.IntegerField()
    date_of_record = models.DateField()
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.IntegerField()

    class Meta:
        db_table = 'env_data'
        managed = True

    def __str__(self):
        return self.record_id
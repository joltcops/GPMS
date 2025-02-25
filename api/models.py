from django.db import models

class household(models.Model):
    household_id = models.CharField(max_length=511, primary_key=True)
    address = models.CharField(max_length=2047)
    income = models.IntegerField()

    class Meta:
        db_table = 'household'  # Use the existing table name
        managed = False  # Prevents Django from creating/modifying this table


class citizen(models.Model):
    citizen_id = models.CharField(max_length=511, primary_key=True)
    name = models.CharField(max_length=511)
    gender = models.CharField(max_length=15)
    dob = models.DateField()
    educational_qualification = models.CharField(max_length=511)
    household = models.ForeignKey(household, on_delete=models.CASCADE, db_column='household_id')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='parent_id')

    class Meta:
        db_table = 'citizen'  # Use the existing table name
        managed = False  # Prevents Django from creating/modifying this table

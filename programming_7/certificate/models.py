from django.db import models


class Certificate(models.Model):
    username = models.CharField(max_length=70)
    birth_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    international_passport = models.CharField(max_length=8)
    vaccine = models.CharField(max_length=70)

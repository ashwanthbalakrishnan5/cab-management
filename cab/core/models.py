from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


# Create your models here.
class DriverProfile(models.Model):
    name = models.CharField(max_length=255)
    mail_id = models.EmailField(max_length=255)
    phone_number = PhoneNumberField()
    available = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CarProfile(models.Model):
    reg_no = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    available = models.BooleanField(default=True)


class Assignment(models.Model):
    car = models.OneToOneField(CarProfile, on_delete=models.CASCADE)
    driver = models.OneToOneField(DriverProfile, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

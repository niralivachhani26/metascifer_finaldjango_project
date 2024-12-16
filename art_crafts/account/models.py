from django.contrib.auth.models import AbstractUser
from django.core.validators import BaseValidator
from django.apps import apps
from django.db import models
import json
from datetime import date
from django.utils.deconstruct import deconstructible
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@deconstructible
class MinAgeValidator(BaseValidator):
    message = ("Age must be at least %(limit_value)d.")
    code = 'min_age'

    def compare(self, a, b):
        return calculate_age(a) < b

def load_states():
    with open('account/indian_states_cities.json', 'r') as f:
        data = json.load(f)
    return [(state, state) for state in data["states"].keys()]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    name = models.CharField(blank=False,max_length=150)
    dob = models.DateField(null=True,blank=True,verbose_name="Date of Birth",validators=[MinAgeValidator(18)])
    contact_no = PhoneNumberField(blank=True, unique=True)
    address = models.TextField(blank=True)

    # Dynamic state choices
    state = models.CharField(max_length=50, choices=load_states(), blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=6, blank=True)

    profile = models.ImageField(blank=True,upload_to='static/images/profile_pictures/')

    USER_TYPE_CHOICES = [
        ('artist', 'Artist'),
        ('customer', 'Customer'),
    ]
    usertype = models.CharField(max_length=20,choices=USER_TYPE_CHOICES, default='customer')

    description = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact_no','address','state','city','zipcode','profile']

    def __str__(self):
        return self.username


# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
    ('M', 'Male'),
    ('F', 'Female')
)


def upload_location(instance, filename):
    return f'users/photos/{instance.get_full_name()}/{filename}'


class User(AbstractUser):
    phone = PhoneNumberField(unique=True, blank=False, null=False)
    gender = models.CharField(choices=GENDER, max_length=6)
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    username = models.CharField(
        unique=True, max_length=100, null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.get_full_name()

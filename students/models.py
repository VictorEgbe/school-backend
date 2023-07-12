from datetime import datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from classes.models import Class


GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


def upload_location(instance, filename):
    return f'students/{instance.name}-{filename}'


class Student(models.Model):
    name = models.CharField(max_length=150)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    student_id = models.CharField(max_length=25, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER)
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    student_phone = PhoneNumberField(null=True, blank=True, unique=True)
    parent_name = models.CharField(max_length=100, null=True, blank=True)
    parent_phone = PhoneNumberField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_age(self):
        year_of_birth = self.date_of_birth.year
        current_year = datetime.now().year
        return current_year - year_of_birth

    def __str__(self):
        return f'{self.name} ({self.student_id})'

    def get_response_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'student_id': self.student_id,
            'student_class': self.student_class.name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'image': self.image.url if self.image else None,
            'student_phone': self.student_phone.as_national if self.student_phone else None,
            'parent_name': self.parent_name,
            'parent_phone': self.parent_phone.as_national,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'age': self.get_age(),
        }

    class Meta:
        ordering = ['name']

from datetime import date

from django.db import models
from accounts.models import User

from departments.models import Department


class Teacher(User):
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_hod = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.get_full_name()}'

    def get_age(self):
        if self.date_of_birth:
            year_of_birth = self.date_of_birth.year
            current_year = date.today().year
            return current_year - year_of_birth
        return None

    class Meta:
        ordering = ('-is_hod', )

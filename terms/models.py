from django.db import models

from years.models import Year


class Term(models.Model):
    name = models.CharField(max_length=100)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} in the year {self.year.name}'

    def get_response_data(self):
        return {
            'id': self.pk,
            'name': self.name,
            'year': self.year.name,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

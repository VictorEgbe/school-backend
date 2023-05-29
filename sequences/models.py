from django.db import models

from classes.models import Class


class Sequence(models.Model):
    name = models.CharField(max_length=100)
    sequence_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        string = f'{self.name} for {self.sequence_class.name} in {self.sequence_class.year.name}'
        return string

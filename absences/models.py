from django.db import models

from students.models import Student
from sequences.models import Sequence


class Absence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=200, null=True, blank=True)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.name} on {self.date}'

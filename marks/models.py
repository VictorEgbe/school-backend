from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from teachers.models import Teacher
from students.models import Student
from subjects.models import Subject
from sequences.models import Sequence


class Mark(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=2, validators=[
                                MinValueValidator(0), MaxValueValidator(20)])
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    is_filled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        student = self.student.name
        student_class = self.student.student_class.name
        subject = self.subject.name
        string = f'{student}: {self.value} on 20 in {student_class} {subject}'
        return string

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from classes.models import Class
from teachers.models import Teacher

COEFFICIENT = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teachers = models.ManyToManyField(Teacher)
    coefficient = models.PositiveSmallIntegerField(
        choices=COEFFICIENT, validators=[MinValueValidator(1), MaxValueValidator(5)])
    code = models.CharField(max_length=10, null=True, blank=True)
    subject_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

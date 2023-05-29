from django.db import models

from years.models import Year


class Class(models.Model):
    name = models.CharField(max_length=100)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} class of {self.year.name}'

    class Meta:
        verbose_name_plural = 'classes'

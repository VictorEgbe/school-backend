from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    HOD_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

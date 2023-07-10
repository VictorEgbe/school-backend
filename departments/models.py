from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hod_id = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pk', )

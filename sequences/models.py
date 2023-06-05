from django.db import models

from terms.models import Term


class Sequence(models.Model):
    name = models.CharField(max_length=100)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        string = f'{self.name}: {self.term.year.name}'
        return string

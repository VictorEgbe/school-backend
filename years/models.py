from django.db import models
from django.utils.translation import gettext_lazy as _


class Year(models.Model):
    name = models.CharField(max_length=60, unique=True, error_messages={
                            "unique": _("Academic Year with this name already exists.")})
    theme = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_response_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'theme': self.theme,
            'is_active': self.is_active
        }

# TODO: Add start date and end date of the year
# TODO: Also, add start year and end year then generate the name using signals

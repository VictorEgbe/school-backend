from django.urls import path

from .views import (
    create_year,
    get_year,
    update_year,
    delete_year,
    get_years
)


urlpatterns = [
    path('create', create_year),
    path('get_years', get_years),
    path('get_year/<int:year_id>', get_year),
    path('update_year/<int:year_id>', update_year),
    path('delete_year/<int:year_id>', delete_year),
]

from django.urls import path

from .views import (
    create_term,
    get_term,
    get_terms,
    update_term,
    delete_term,
    deactivate_term
)

urlpatterns = [
    path('get_terms', get_terms),
    path('create_term/<int:year_id>', create_term),
    path('deactivate_term/<int:term_id>', deactivate_term),
    path('delete_term/<int:term_id>', delete_term),
    path('get_term/<int:term_id>', get_term),
    path('update_term/<int:term_id>/<int:new_year_id>', update_term),
]

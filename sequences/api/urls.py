from django.urls import path

from .views import (
    create_sequence,
    get_sequences,
    get_sequences_term,
    get_sequence,
    delete_sequence,
    update_sequence,
    deactivate_sequence
)

urlpatterns = [
    path('', get_sequences),
    path('create/<int:term_id>', create_sequence),
    path('delete/<int:sequence_id>', delete_sequence),
    path('deactivate', deactivate_sequence),
    path('update/<int:term_id>', update_sequence),
    path('get_sequence/<int:sequence_id>', get_sequence),
    path('get_sequences_term/<int:term_id>', get_sequences_term),
]

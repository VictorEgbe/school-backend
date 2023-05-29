from django.urls import path

from .views import (
    create_sequence,
    get_sequences,
    get_sequence,
    delete_sequence,
    update_sequence,
    deactivate_sequence
)

urlpatterns = [
    path('', get_sequences),
    path('create', create_sequence),
    path('delete', delete_sequence),
    path('deactivate', deactivate_sequence),
    path('update', update_sequence),
    path('get_sequence/<int:sequence_id>', get_sequence),
]

from django.urls import path

from .views import (
    create_or_update_absences,
    get_total_sequence_absences,
    get_total_term_absences
)

urlpatterns = [
    path('create_or_update_absences', create_or_update_absences),
    path('get_total_sequence_absences/<str:student_id>/<int:sequence_id>',
         get_total_sequence_absences),

    path('get_total_term_absences/<str:student_id>/<int:term_id>',
         get_total_term_absences),
]

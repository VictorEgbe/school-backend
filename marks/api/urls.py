from django.urls import path

from .views import (
    create_mark,
    get_marks_for_student
)

urlpatterns = [
    path('create_mark/<str:student_id>/<int:subject_id>', create_mark),
    path('get_marks_for_student/<str:student_id>', get_marks_for_student),
]

from django.urls import path

from .views import (
    create_or_update_mark,
    get_marks_for_student,
    get_all_marks_for_students_in_class,
    update_mark
)

urlpatterns = [
    path('create_or_update_mark/<int:class_id>/<int:subject_id>',
         create_or_update_mark),
    path('get_marks_for_student/<str:student_id>', get_marks_for_student),
    path('get_all_marks_for_students_in_class/<str:class_id>',
         get_all_marks_for_students_in_class),
    path('update_mark/<int:mark_id>', update_mark),

]

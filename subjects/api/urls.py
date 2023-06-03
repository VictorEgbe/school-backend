from django.urls import path

from .views import (
    add_teacher_to_subject,
    create_subject_in_class,
    delete_subject,
    get_single_subject_in_a_class,
    get_all_subjects_in_a_class,
    get_all_subjects_by_a_teacher,
    remove_teacher_to_subject,
    update_subject,
)

urlpatterns = [
    path('get_subject_in_a_class/<int:class_id>', get_all_subjects_in_a_class),
    path('create_subject/<int:class_id>/<int:teacher_id>', create_subject_in_class),
    path('add_teacher_to_subject/<int:subject_id>/<int:teacher_id>',
         add_teacher_to_subject),
    path('remove_teacher_to_subject/<int:subject_id>/<int:teacher_id>',
         remove_teacher_to_subject),
    path('get_subject/<int:subject_id>', get_single_subject_in_a_class),
    path('get_teacher_subjects/<int:teacher_id>', get_all_subjects_by_a_teacher),
    path('update_subject/<int:subject_id>', update_subject),
    path('delete_subject/<int:subject_id>', delete_subject),
]

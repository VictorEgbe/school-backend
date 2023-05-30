from django.urls import path

from .views import (
    create_student,
    get_all_students_in_class,
    get_all_students_in_school,
    get_student,
    delete_student,
    update_student
)


urlpatterns = [
    path('get_all', get_all_students_in_school),
    path('get_in_class/<int:class_id>', get_all_students_in_class),
    path('get_student/<int:student_id>', get_student),
    path('create_student/<int:class_id>', create_student),
    path('delete_student/<int:student_id>', delete_student),
    path('update_student/<int:student_id>/<int:new_class_id>', update_student),

]

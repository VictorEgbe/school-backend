from django.urls import path

from .views import (
    create_teacher,
    delete_teacher,
    get_all_teachers,
    get_teacher,
    update_teacher,
    teacher_password_change
)

urlpatterns = [
    path('', get_all_teachers),
    path('create_teacher/<int:department_id>', create_teacher),
    path('get_teacher/<int:teacher_id>', get_teacher),
    path('delete_teacher/<int:teacher_id>', delete_teacher),
    path('teacher_password_change/<int:teacher_id>', teacher_password_change),
    path('update_teacher/<int:teacher_id>/<int:new_department_id>', update_teacher),
]

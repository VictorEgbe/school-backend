from django.urls import path

from .views import (
    create_teacher,
    delete_teacher,
    get_all_teachers,
    get_teacher,
    update_teacher,
)

urlpatterns = [
    path('', get_all_teachers),
    path('create_teacher/<int:department_id>', create_teacher),
    path('get_teacher/<int:teacher_id>', get_teacher),
    path('delete_teacher/<int:teacher_id>', delete_teacher),
    path('update_teacher/<int:teacher_id>/<int:department_id>', update_teacher),
]

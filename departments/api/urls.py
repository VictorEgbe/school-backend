from django.urls import path

from .views import (
    create_department,
    delete_department,
    get_all_departments,
    get_department,
    update_department,
)

urlpatterns = [
    path('', get_all_departments),
    path('get_department/<int:department_id>', get_department),
    path('create_department', create_department),
    path('delete_department/<int:department_id>', delete_department),
    path('update_department/<int:department_id>', update_department),

]

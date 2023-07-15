from django.urls import path


from .views import dashboard, get_departments_ids_and_names, get_teacher_update_info


urlpatterns = [
    path('dashboard', dashboard),
    path('get_departments_ids_and_names', get_departments_ids_and_names),
    path('get_teacher_update_info/<int:teacher_id>', get_teacher_update_info),
]

from django.urls import path


from .views import dashboard, get_departments_ids_and_names


urlpatterns = [
    path('dashboard', dashboard),
    path('get_departments_ids_and_names', get_departments_ids_and_names),
]

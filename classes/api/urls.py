from django.urls import path

from .views import (
    create_class,
    get_class,
    get_classes,
    delete_class,
    update_class
)


urlpatterns = [
    path('', get_classes),
    path('get_class/<int:class_id>', get_class),
    path('create', create_class),
    path('update/<int:class_id>/<int:new_year_id>', update_class),
    path('delete/<int:class_id>', delete_class),
]

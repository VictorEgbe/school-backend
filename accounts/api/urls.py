from django.urls import path
from knox.views import LogoutAllView, LogoutView
from .views import (
    sign_up,
    sign_in,
    profile,
    update_user,
    delete_user,
    get_all_users,
    change_user_password

)

urlpatterns = [
    path('sign_up', sign_up),
    path('sign_in', sign_in),
    path('sign_out', LogoutView.as_view()),
    path('sign_out_all', LogoutAllView.as_view()),
    path('profile/<int:user_id>', profile),
    path('update_user/<int:user_id>', update_user),
    path('delete_user/<int:user_id>', delete_user),
    path('all_users', get_all_users),
    path('change_user_password/<int:user_id>', change_user_password),
]

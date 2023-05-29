
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/accounts/', include('accounts.api.urls')),
    path('api/classes/', include('classes.api.urls')),
    path('api/terms/', include('terms.api.urls')),
    path('api/years/', include('years.api.urls')),
    path('admin/', admin.site.urls),
]

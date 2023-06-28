
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/accounts/', include('accounts.api.urls')),
    path('api/absences/', include('absences.api.urls')),
    path('api/classes/', include('classes.api.urls')),
    path('api/departments/', include('departments.api.urls')),
    path('api/marks/', include('marks.api.urls')),
    path('api/others/', include('others.api.urls')),
    path('api/sequences/', include('sequences.api.urls')),
    path('api/students/', include('students.api.urls')),
    path('api/subjects/', include('subjects.api.urls')),
    path('api/teachers/', include('teachers.api.urls')),
    path('api/terms/', include('terms.api.urls')),
    path('api/years/', include('years.api.urls')),
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('current.urls', namespace='current')),
    path('admin/', admin.site.urls),
]

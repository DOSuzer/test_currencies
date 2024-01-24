from django.urls import path
from current.views import current_usd

app_name = 'current'

urlpatterns = [
    path('get-current-usd/', current_usd, name='current_usd'),
]

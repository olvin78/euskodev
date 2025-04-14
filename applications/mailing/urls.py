# mailing/urls.py
from django.urls import path
from .views import mailing_view

app_name = 'mailing_app'

urlpatterns = [
    path('enviar/', mailing_view, name='manual'),
]

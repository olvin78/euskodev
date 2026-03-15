from django.urls import path
from .views import ContactListView, AddContactView

app_name = 'contact_app'

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('add/', AddContactView.as_view(), name='add_contact'),
]

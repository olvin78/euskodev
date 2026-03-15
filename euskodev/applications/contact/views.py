from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Contact
from .forms import ContactForm
from django.urls import reverse_lazy

# Vista para la lista de contactos (filtrada)
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ContactListView(StaffRequiredMixin, ListView):
    model = Contact
    template_name = 'contact/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        contacts = Contact.objects.all()
        if query:
            contacts = contacts.filter(
                Q(name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query)
            )
        return contacts

# Vista para agregar un nuevo contacto
class AddContactView(StaffRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/add_contact.html'
    success_url = reverse_lazy('contact_app:contact_list')

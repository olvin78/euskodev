from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView
)
from .models import Company
from django.shortcuts import redirect
from django.contrib import messages


class ListCompaniesView(UserPassesTestMixin, ListView):
    model = Company
    template_name = 'companies/list_companies.html'
    context_object_name = 'datos'
    ordering = [
        '-id'
    ]

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Solo el equipo staff puede acceder a esta página.")
        return redirect("home_app:home")

class MapCompaniesView(UserPassesTestMixin, ListView):
    model = Company
    template_name = 'companies/map_companies.html'
    context_object_name = 'datos'
    ordering = [
        '-id'
    ]

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Solo el equipo staff puede acceder a esta página.")
        return redirect("home_app:home")

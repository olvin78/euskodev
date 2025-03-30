from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView
)
from .models import Company


class ListCompaniesView(ListView):
    model = Company
    template_name = 'companies/list_companies.html'
    context_object_name = 'datos'
    ordering = [
        '-id'
    ]

class MapCompaniesView(ListView):
    model = Company
    template_name = 'companies/map_companies.html'
    context_object_name = 'datos'
    ordering = [
        '-id'
    ]

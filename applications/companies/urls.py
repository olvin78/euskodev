from os import name
from django.urls import include, path
from .views import ListCompaniesView, MapCompaniesView
from django.conf.urls import handler404
from . import views

app_name = 'companies_app'

handler404 ='applications.home.views.custom_404'

urlpatterns = [
    path('lista/',
        views.ListCompaniesView.as_view(),
        name='list_companies',
    ),
    path('',
        views.MapCompaniesView.as_view(),
        name='map_companies',
    ),
    path('mapa/',
        views.MapCompaniesView.as_view(),
        name='map_companies',
    ),

]
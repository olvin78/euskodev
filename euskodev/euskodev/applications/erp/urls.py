from os import name
from django.urls import include, path
from .views import BudgetCreateView
from . import views
from django.conf.urls import handler404
from django.shortcuts import get_object_or_404

from .views import BudgetDetailView, add_client, BudgetUpdateView  # 🔹 Agrega `update_budget`


app_name = 'dashboard_app'

handler404 ='applications.home.views.custom_404'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),
    path('budget/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),
    path('add-client/', add_client, name='add_client'),
    path('delete-item/<int:item_id>/', views.delete_budget_item, name='delete_item'),
    path('budget/update/<int:pk>/', BudgetUpdateView.as_view(), name='update_budget'),
    path('budget/list/', views.BudgetListView.as_view(), name='budget_list'),
    path('budget/create/', BudgetCreateView.as_view(), name='budget_create'),
    path('budget/create/', BudgetCreateView.as_view(), name='create_budget'),
]
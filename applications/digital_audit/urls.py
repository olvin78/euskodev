from django.urls import path
from .views import DigitalizationAssessmentView
from django.views.generic import TemplateView

app_name = 'digital_audit_app'  # este nombre DEBE coincidir con reverse_lazy()

urlpatterns = [
    path('', DigitalizationAssessmentView.as_view(), name='form'),
    path('gracias/', TemplateView.as_view(template_name='digital_audit/thank_you.html'), name='thank_you'),
]
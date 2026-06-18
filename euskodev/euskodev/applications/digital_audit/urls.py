from django.urls import path
from .views import DigitalizationAssessmentView, procesar_test
from django.views.generic import TemplateView

app_name = 'digital_audit_app'

urlpatterns = [
    path('', DigitalizationAssessmentView.as_view(), name='form'),
    path('procesar/', procesar_test, name='procesar'),
    path('gracias/', TemplateView.as_view(template_name='digital_audit/thank_you.html'), name='thank_you'),
]

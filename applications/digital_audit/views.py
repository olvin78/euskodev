from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .forms import DigitalizationAssessmentForm
from .models import DigitalizationAssessment
# Create your views here.

class DigitalizationAssessmentView(FormView):
    template_name = 'digital_audit/form.html'
    form_class = DigitalizationAssessmentForm
    success_url = reverse_lazy('digital_audit_app:thank_you')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        context['sections'] = [
            ("Presencia Online", [form['has_website'], form['website_responsive'], form['seo_optimized'], form['has_google_business'], form['uses_analytics']]),
            ("Redes Sociales y Marketing", [form['active_social_media'], form['does_ads'], form['uses_newsletters'], form['uses_crm'], form['has_lead_campaigns']]),
            ("Comercio Electrónico", [form['sells_online'], form['accepts_online_payments'], form['has_booking_system'], form['has_cart_system']]),
            ("Gestión Interna y Procesos", [form['uses_erp'], form['uses_digital_invoicing'], form['automates_processes'], form['uses_collab_software'], form['has_backup_system']]),
            ("Comunicación y Atención al Cliente", [form['has_chatbot'], form['uses_whatsapp'], form['has_support_system'], form['quick_response_channels']]),
            ("Aplicaciones y Movilidad", [form['has_mobile_app'], form['has_private_area'], form['employees_mobile_access'], form['uses_productivity_apps']]),
            ("Análisis y Datos", [form['analyzes_metrics'], form['uses_dashboards'], form['tracks_kpis']]),
            ("Ciberseguridad y Cumplimiento", [form['has_ssl'], form['secure_passwords'], form['gdpr_compliant'], form['performs_security_audits']]),
        ]
        return context


class ThankYouBecaudeTheTestView(TemplateView):
    template_name= 'digital_audit/thank_you.html'

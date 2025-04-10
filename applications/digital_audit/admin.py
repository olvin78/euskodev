from django.contrib import admin
from .models import DigitalizationAssessment

@admin.register(DigitalizationAssessment)
class DigitalizationAssessmentAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_email', 'contact_name', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('company_name', 'company_email', 'contact_name')
    readonly_fields = ('submitted_at',)

    fieldsets = (
        ('Datos de contacto', {
            'fields': ('company_name', 'contact_name', 'company_email', 'business_activity')
        }),
        ('Presencia Online', {
            'fields': ('has_website', 'website_responsive', 'seo_optimized', 'has_google_business', 'uses_analytics')
        }),
        ('Redes Sociales y Marketing', {
            'fields': ('active_social_media', 'does_ads', 'uses_newsletters', 'uses_crm', 'has_lead_campaigns')
        }),
        ('Comercio Electrónico', {
            'fields': ('sells_online', 'accepts_online_payments', 'has_booking_system', 'has_cart_system')
        }),
        ('Gestión Interna y Procesos', {
            'fields': ('uses_erp', 'uses_digital_invoicing', 'automates_processes', 'uses_collab_software', 'has_backup_system')
        }),
        ('Comunicación y Atención al Cliente', {
            'fields': ('has_chatbot', 'uses_whatsapp', 'has_support_system', 'quick_response_channels')
        }),
        ('Aplicaciones y Movilidad', {
            'fields': ('has_mobile_app', 'has_private_area', 'employees_mobile_access', 'uses_productivity_apps')
        }),
        ('Análisis y Datos', {
            'fields': ('analyzes_metrics', 'uses_dashboards', 'tracks_kpis')
        }),
        ('Ciberseguridad y Cumplimiento', {
            'fields': ('has_ssl', 'secure_passwords', 'gdpr_compliant', 'performs_security_audits')
        }),
        ('Meta', {
            'fields': ('submitted_at',)
        }),
    )

from django.db import models
from django.utils.translation import gettext_lazy as _

class DigitalizationAssessment(models.Model):
    # Opciones para campos booleanos con null
    BOOL_CHOICES = [
        (True, _("Sí")),
        (False, _("No")),
        (None, _("No lo sé")),
    ]

    # Datos de contacto
    company_name = models.CharField(_("Nombre de la empresa"), max_length=255)
    contact_name = models.CharField(_("Nombre de contacto"), max_length=255)
    company_email = models.EmailField(_("Correo electrónico de contacto"))
    contact_tel = models.CharField(_("Teléfono de contacto (opcional)"), max_length=15, blank=True, null=True)
    business_activity = models.CharField(("¿A qué se dedica la empresa?"), max_length=300, blank=True, null=True)

    # 1. Presencia Online
    has_website = models.BooleanField(_("La empresa tiene una página web corporativa"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    website_responsive = models.BooleanField(_("La web es responsive y se adapta a móviles"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    seo_optimized = models.BooleanField(_("La web está optimizada para buscadores (SEO)"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    has_google_business = models.BooleanField(_("La empresa tiene ficha en Google Business"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_analytics = models.BooleanField(_("Utiliza herramientas como Google Analytics"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    # 2. Redes Sociales y Marketing Digital
    active_social_media = models.BooleanField(_("Tiene presencia activa en redes sociales"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    does_ads = models.BooleanField(_("Hace campañas en redes o Google Ads"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_newsletters = models.BooleanField(_("Envía newsletters o emails promocionales"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_crm = models.BooleanField(_("Utiliza un CRM para gestión de contactos/clientes"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    has_lead_campaigns = models.BooleanField(_("Realiza campañas de captación de leads"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    # 3. Comercio Electrónico
    sells_online = models.BooleanField(_("Vende productos o servicios online"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    accepts_online_payments = models.BooleanField(_("Acepta pagos digitales"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    has_booking_system = models.BooleanField(_("Tiene un sistema de reservas online"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    has_cart_system = models.BooleanField(_("Tiene carrito de compras en su web"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    # 4. Gestión Interna y Procesos
    uses_erp = models.BooleanField(_("Utiliza un ERP para la gestión interna"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_digital_invoicing = models.BooleanField(_("Usa facturación digital"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    automates_processes = models.BooleanField(_("Automatiza procesos repetitivos"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_collab_software = models.BooleanField(_("Utiliza software colaborativo"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    has_backup_system = models.BooleanField(_("Tiene copias de seguridad automatizadas"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    # 5. Comunicación y Atención al Cliente
    has_chatbot = models.BooleanField(_("Tiene un chatbot o asistente virtual"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_whatsapp = models.BooleanField(_("Utiliza WhatsApp Business u otro canal directo"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    has_support_system = models.BooleanField(_("Tiene sistema de soporte o tickets"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    quick_response_channels = models.BooleanField(_("Responde rápidamente en canales digitales"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    # 6. Aplicaciones y Movilidad
    has_mobile_app = models.BooleanField(_("Tiene una app móvil propia"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    has_private_area = models.BooleanField(_("Tiene una zona privada o funcionalidades especiales"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    employees_mobile_access = models.BooleanField(_("Los empleados pueden trabajar desde el móvil"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_productivity_apps = models.BooleanField(_("Utiliza apps móviles de productividad"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    # 7. Análisis y Datos
    analyzes_metrics = models.BooleanField(_("Analiza métricas de ventas y clientes"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    uses_dashboards = models.BooleanField(_("Utiliza dashboards para decisiones"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    tracks_kpis = models.BooleanField(_("Mide objetivos digitales (KPI)"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    # 8. Ciberseguridad y Cumplimiento
    has_ssl = models.BooleanField(_("Su web tiene certificado SSL"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    secure_passwords = models.BooleanField(_("Usa contraseñas seguras y doble factor"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    gdpr_compliant = models.BooleanField(_("Está adaptado a la normativa RGPD"), null=True, blank=True, choices=BOOL_CHOICES, default=None)
    performs_security_audits = models.BooleanField(_("Realiza auditorías de seguridad"), null=True, blank=True, choices=BOOL_CHOICES, default=None)

    submitted_at = models.DateTimeField(_("Fecha de envío"), auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.company_email}) - {self.submitted_at.date()}"

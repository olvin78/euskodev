from django.db import models

class Company(models.Model):
    name = models.CharField("Nombre de la empresa", max_length=255)
    legal_name = models.CharField("Razón social", max_length=255, blank=True, null=True)
    vat_number = models.CharField("CIF/NIF", max_length=50, blank=True, null=True)

    email = models.EmailField("Email de contacto", blank=True, null=True)
    phone = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    website = models.URLField("Sitio web", blank=True, null=True)

    address = models.CharField("Dirección", max_length=255, blank=True, null=True)
    city = models.CharField("Ciudad", max_length=100, blank=True, null=True)
    postal_code = models.CharField("Código postal", max_length=20, blank=True, null=True)
    country = models.CharField("País", max_length=100, blank=True, null=True)

    logo = models.ImageField("Logo de la empresa", upload_to="companies/logos/", blank=True, null=True)

    latitude = models.CharField("Latitud", max_length=30, blank=True, null=True)
    longitude = models.CharField("Longitud", max_length=30,blank=True, null=True)

    has_website = models.BooleanField("¿Tiene página web?", null=True, blank=True, default=None)
    has_mobile_app = models.BooleanField("¿Tiene app móvil?", null=True, blank=True, default=None)
    has_custom_software = models.BooleanField("¿Usa software propio?", null=True, blank=True, default=None)
    uses_ai = models.BooleanField("¿Utiliza inteligencia artificial?", null=True, blank=True, default=None)
    is_competition_company = models.BooleanField("¿Es competencia de Euskdoev?", null=True, blank=True, default=None)
    manager_name = models.CharField("Nombre del gerente", max_length=255, blank=True, null=True)
    manager_phone = models.CharField("Teléfono del gerente", max_length=50, blank=True, null=True)
    manager_email = models.EmailField("Email del gerente", blank=True, null=True)

    visited = models.BooleanField("¿Ha sido visitada?", default=False)
    visit_date = models.DateField("Fecha de visita", blank=True, null=True)

    comments = models.TextField("Comentarios", blank=True, null=True)

    is_active = models.BooleanField("¿Activa?", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["name"]

    def __str__(self):
        return self.name

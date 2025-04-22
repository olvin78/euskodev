from django.db import models
from django.utils import timezone
from applications.companies.models import Company  # Importa Company desde la app 'companies'


class Contact(models.Model):
    first_name = models.CharField("Primer nombre", max_length=100)
    second_name = models.CharField("Segundo nombre", max_length=100, blank=True, null=True)
    last_name = models.CharField("Primer apellido", max_length=100)
    second_last_name = models.CharField("Segundo apellido", max_length=100, blank=True, null=True)
    
    phone = models.CharField("Teléfono principal", max_length=20)
    secondary_phone = models.CharField("Teléfono secundario", max_length=20, blank=True, null=True)
    
    email = models.EmailField("Correo electrónico", blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con la empresa
    
    position = models.CharField("Puesto de trabajo", max_length=100, blank=True, null=True)
    address = models.CharField("Dirección", max_length=300, blank=True, null=True)
    city = models.CharField("Ciudad", max_length=100, blank=True, null=True)
    state = models.CharField("Estado", max_length=100, blank=True, null=True)
    country = models.CharField("País", max_length=100, blank=True, null=True)
    
    # Campos adicionales
    nif = models.CharField("NIF/CIF", max_length=50, blank=True, null=True)  # NIF/CIF de la persona o empresa
    date_of_birth = models.DateField("Fecha de nacimiento", blank=True, null=True)  # Fecha de nacimiento (opcional)
    gender = models.CharField("Género", max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], blank=True, null=True)
    nationality = models.CharField("Nacionalidad", max_length=100, blank=True, null=True)  # Nacionalidad
    
    notes = models.TextField("Notas", blank=True, null=True)
    date_added = models.DateTimeField("Fecha de alta", default=timezone.now)  # Asegúrate de que esté correctamente configurado

    
    # Campos de contacto adicional
    manager_name = models.CharField("Nombre del gerente", max_length=255, blank=True, null=True)  # Nombre del gerente
    manager_phone = models.CharField("Teléfono del gerente", max_length=50, blank=True, null=True)  # Teléfono del gerente
    manager_email = models.EmailField("Email del gerente", blank=True, null=True)  # Email del gerente
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
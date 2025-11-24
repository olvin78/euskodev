from django.db import models
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import timedelta


# ===========================
# Modelo para datos de la empresa (Datos del Profesional)
# ===========================
class CompanyInfo(models.Model):
    nombre = models.CharField(max_length=100, default="Olvin Duarte")
    nombre_comercial = models.CharField(max_length=100, default="Euskodev")
    nif = models.CharField(max_length=20, blank=True, null=True)
    direccion_fiscal = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web = models.URLField(blank=True, null=True)

    # Opciones de banco
    BANCOS_CHOICES = [
        ('CAIXABANK', 'CaixaBank'),
        ('SANTANDER', 'Banco Santander'),
        ('BBVA', 'BBVA'),
        ('SABADELL', 'Banco Sabadell'),
        ('ING', 'ING España'),
        ('BANKINTER', 'Bankinter'),
        ('OPENBANK', 'OpenBank'),
        ('EVOBANK', 'EVO Banco'),
        ('ABANCA', 'ABANCA'),
        ('OTRO', 'Otro / Personalizado'),
    ]
    banco = models.CharField(max_length=50, choices=BANCOS_CHOICES, blank=True, null=True)

    # Opciones de forma de pago
    PAGO_CHOICES = [
        ('TRANSFERENCIA', 'Transferencia bancaria'),
        ('BIZUM', 'Bizum'),
        ('PAYPAL', 'PayPal'),
        ('TPV', 'TPV Virtual (Tarjeta)'),
        ('STRIPE', 'Stripe (Tarjeta / Apple Pay / Google Pay)'),
    ]
    forma_pago = models.CharField(max_length=50, choices=PAGO_CHOICES, default='TRANSFERENCIA')

    cuenta_bancaria = models.CharField(max_length=50, blank=True, null=True)

    # Control de visibilidad en presupuesto
    mostrar_datos_pago_en_presupuesto = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_comercial


# ===========================
# Modelo para los Clientes
# ===========================
class Client(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    nif = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.nombre if self.nombre else "Cliente sin nombre"


# ===========================
# Modelo para Presupuestos
# ===========================
class Budget(models.Model):
    cliente = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True)
    agente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey('CompanyInfo', on_delete=models.SET_NULL, null=True, blank=True)

    fecha_creacion = models.DateField(auto_now_add=True, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    impuesto_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, blank=True, null=True)

    numero_presupuesto_manual = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name="Número de presupuesto (editable)"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.numero_presupuesto_manual and self.id:
            self.numero_presupuesto_manual = self.id + 70
            super().save(update_fields=['numero_presupuesto_manual'])

        if not self.fecha_vencimiento and self.fecha_creacion:
            self.fecha_vencimiento = self.fecha_creacion + timedelta(days=15)
            super().save(update_fields=['fecha_vencimiento'])

    @property
    def numero_presupuesto(self):
        return self.numero_presupuesto_manual or (self.id + 70 if self.id else "—")

    @property
    def calcular_subtotal(self):
        subtotal = self.items.aggregate(total=Sum('subtotal'))['total']
        return subtotal if subtotal is not None else Decimal(0)

    @property
    def calcular_impuestos(self):
        return (self.calcular_subtotal * self.impuesto_porcentaje) / Decimal(100)

    @property
    def calcular_total_con_impuestos(self):
        return self.calcular_subtotal + self.calcular_impuestos

    def __str__(self):
        return f"Presupuesto #{self.numero_presupuesto} - {self.cliente}"


# ===========================
# Modelo para Ítems del Presupuesto
# ===========================
class BudgetItem(models.Model):
    presupuesto = models.ForeignKey("Budget", on_delete=models.CASCADE, related_name="items")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=1, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        cantidad = Decimal(self.cantidad) if self.cantidad else Decimal(1)
        precio_unitario = Decimal(self.precio_unitario) if self.precio_unitario else Decimal(0.00)
        descuento = Decimal(self.descuento) if self.descuento else Decimal(0.00)

        total_bruto = cantidad * precio_unitario
        descuento_aplicado = (descuento / Decimal(100)) * total_bruto
        self.subtotal = total_bruto - descuento_aplicado

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descripcion} - Presupuesto #{self.presupuesto.numero_presupuesto}"

from django.db import models
from decimal import Decimal
from django.db.models import Sum  # ✅ IMPORTA SUM AQUÍ
from django.contrib.auth.models import User  # 👈 Importa el modelo de usuario
# Modelo para los clientes
from django.db import models

class Client(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)  
    nif = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True, blank=True, null=True)  # 📌 Agrega esto si falta

    def __str__(self):
        return self.nombre if self.nombre else "Cliente sin nombre"


# Modelo para los presupuestos


class Budget(models.Model):
    cliente = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True)
    agente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    impuesto_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, blank=True, null=True)

    @property
    def numero_presupuesto(self):
        """Devuelve el número del presupuesto empezando desde 71, 72, 73..."""
        return self.id + 70 if self.id else None

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



class BudgetItem(models.Model):
    presupuesto = models.ForeignKey("Budget", on_delete=models.CASCADE, related_name="items")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=1)  # ✔️ limpio y seguro
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✔️ con default
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        cantidad = Decimal(self.cantidad)
        precio_unitario = Decimal(self.precio_unitario) if self.precio_unitario else Decimal(0)
        descuento = Decimal(self.descuento) if self.descuento else Decimal(0)

        total_bruto = cantidad * precio_unitario
        descuento_aplicado = (descuento / Decimal(100)) * total_bruto
        self.subtotal = total_bruto - descuento_aplicado

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descripcion} - Presupuesto #{self.presupuesto.numero_presupuesto}"

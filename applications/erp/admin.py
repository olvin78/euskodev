from django.contrib import admin
from .models import Client, Budget, BudgetItem

# 1️⃣ Configuración del Admin para Clientes
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'nif', 'email', 'telefono', 'ciudad', 'codigo_postal')
    search_fields = ('nombre', 'empresa', 'nif', 'email', 'telefono')
    list_filter = ('ciudad',)
    ordering = ('nombre',)

# 2️⃣ Configuración Inline para los ítems del Presupuesto (para que aparezcan dentro del presupuesto)
class BudgetItemInline(admin.TabularInline):  
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('en_proceso', 'En Proceso'),
    ]
    model = BudgetItem
    extra = 1  # Muestra una fila vacía para agregar nuevos ítems automáticamente
    fields = ('descripcion', 'cantidad', 'precio_unitario', 'descuento', 'subtotal')  # 🔹 Agregado `descuento`
    readonly_fields = ('subtotal',)  # 🔹 Sigue siendo de solo lectura

# 3️⃣ Configuración del Admin para Presupuestos
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'id', 'fecha_creacion', 'total')
    search_fields = ('id', 'cliente__nombre')
    list_filter = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)
    autocomplete_fields = ('cliente',)
    inlines = [BudgetItemInline]  # 🔹 Muestra los ítems dentro del presupuesto

# 4️⃣ Configuración del Admin para los Ítems del Presupuesto (separado, para búsqueda y filtros)
@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('presupuesto', 'descripcion', 'cantidad', 'precio_unitario', 'descuento', 'subtotal')
    search_fields = ('descripcion', 'presupuesto__id')
    list_filter = ('presupuesto',)

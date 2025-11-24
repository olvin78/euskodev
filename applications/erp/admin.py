from django.contrib import admin
from .models import Client, Budget, BudgetItem, CompanyInfo

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
    list_display = ('numero_presupuesto', 'cliente', 'fecha_creacion', 'fecha_vencimiento', 'total')
    search_fields = ('numero_presupuesto_manual', 'cliente__nombre')
    list_filter = ('fecha_creacion', 'fecha_vencimiento')
    ordering = ('-fecha_creacion',)
    autocomplete_fields = ('cliente',)
    inlines = [BudgetItemInline]

    fieldsets = (
        ("Información del Cliente", {
            'fields': ('cliente', 'agente')
        }),
        ("Detalles del Presupuesto", {
            'fields': ('descripcion', 'numero_presupuesto_manual')
        }),
        ("Fechas", {
            'fields': ('fecha_creacion', 'fecha_vencimiento')
        }),
        ("Totales", {
            'fields': ('total', 'impuesto_porcentaje')
        }),
    )

    readonly_fields = ('fecha_creacion',)


# 4️⃣ Configuración del Admin para los Ítems del Presupuesto (separado, para búsqueda y filtros)
@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('id','presupuesto', 'descripcion', 'cantidad', 'precio_unitario', 'descuento', 'subtotal')
    search_fields = ('descripcion', 'presupuesto__id')
    list_filter = ('presupuesto',)





@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'nombre', 'email', 'telefono', 'nif', 'forma_pago', 'banco')
    search_fields = ('nombre', 'nombre_comercial', 'nif', 'email')
    list_filter = ('banco', 'forma_pago')
    
    fieldsets = (
        ("🧾 Información fiscal y comercial", {
            'fields': ('nombre', 'nombre_comercial', 'nif', 'direccion_fiscal')
        }),
        ("📞 Contacto", {
            'fields': ('telefono', 'email', 'web')
        }),
        ("💳 Datos bancarios", {
            'fields': ('banco', 'cuenta_bancaria', 'forma_pago')
        }),
        ("⚙️ Opciones de visualización", {
            'fields': ('mostrar_datos_pago_en_presupuesto',)
        }),
    )

from django.contrib import admin
from .models import Blog


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ("fecha_hora", "titulo", "imagen", "autor", "cuerpo")
admin.site.register(Blog,BlogAdmin)
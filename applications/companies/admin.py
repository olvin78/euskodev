from django.contrib import admin
from applications.companies.models import Company

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "city")
admin.site.register(Company,CompanyAdmin)
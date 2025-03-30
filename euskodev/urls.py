from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.i18n import i18n_patterns
from applications import home
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from applications.home.views import formulario_contactar  # ✅ Correcto si la vista está en `home`



urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Fuera de i18n_patterns (corregido) 
    path('erp/', include('applications.erp.urls')),  # Mantén tu aplicación dentro de i18n_patterns
    path('empresas/', include('applications.companies.urls')),
 
    path("ads.txt",
         RedirectView.as_view(url=staticfiles_storage.url("ads.txt")),),

]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),  # Para acceder a Rosetta
    ]

urlpatterns += i18n_patterns(
    path('', include('applications.home.urls')),  # Mantén tu aplicación dentro de i18n_patterns
    path("accounts/", include("allauth.urls")), # <-- esta debe estar
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'applications.home.views.custom_404'



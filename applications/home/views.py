from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView
)

from .models import Blog

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from applications.home.models import Blog

from django.shortcuts import render
from django.http import HttpResponse
import requests


def formulario_contactar(request):
    if request.method == "POST":
        print("post")
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        company = request.POST.get("company", "")
        message = request.POST.get("message", "")
        recaptcha_response = request.POST.get("g-recaptcha-response")
        print("POST con estos datos:",name,email,phone,company,message,recaptcha_response)

        # Enviar correo con los datos ingresados desde la web
        asunto = f"Tu Asistente Inteligente Nuevo mensaje de contacto de {name}"
        contenido = (
            f"Nombre: {name}\n"
            f"Email: {email}\n"
            f"Teléfono: {phone}\n"
            f"Empresa: {company}\n"
            f"Mensaje:\n{message}"
        )

        try:
            print("Try de la función send_mail")
            send_mail(
                asunto,
                contenido,
                settings.EMAIL_HOST_USER,  # Remitente
                ["euskodev@gmail.com"],  # Cambia por el correo real
                fail_silently=False,
            )
            print("Enviado email")
            messages.success(request, "Tu mensaje ha sido enviado con éxito.")
            return redirect("home_app:home")

        except Exception as e:
            print(f"Error en send_mail: {e}")  # Esto imprimirá el error en la terminal
            messages.error(request, f"Error al enviar el correo: {str(e)}")
            return render(request, "home/index.html", {
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "message": message
            })

    return redirect("home_app:home")


class HomePageView(ListView):
    template_name = "home/index.html"
    model = Blog
    context_object_name = 'entradas_blog'
    def get_queryset(self):
        # Obtenemos el queryset original
        queryset = super().get_queryset()
        # Filtramos y seleccionamos el primer objeto
        first_item = queryset.first()
        # Si no hay objetos en el queryset, devolvemos un queryset vacío
        if first_item is None:
            return queryset.none()
        # Devolvemos un queryset que contiene solo el primer objeto
        return queryset.order_by('-id')[:3]


class PoliticasdeprivacidadView(TemplateView):
    template_name = "home/Politicas_de_privacidad.html"


class Politicas_de_cookiesView(TemplateView):
    template_name = "home/politicas_de_cookies.html"


class AvisolegalView(TemplateView):
    template_name = "home/Aviso_legal.html"


class BlogView(ListView):
    model = Blog
    template_name = 'home/Blog.html'
    context_object_name = 'entradas_blog'
    ordering = [
        '-fecha_hora'
    ]

class BlogDetailView(DetailView):
    model = Blog # Especifica el modelo Blog
    template_name = 'home/articulo_completo.html' # Define el template "articulo_completo.html"
    context_object_name = 'articulo'

class AteneaGastronomicaView(TemplateView):
    template_name = "portfolio/atenea-gastronomica/index.html"

class LaMaisonDuBordeauxView(TemplateView):
    template_name = "portfolio/la-maison-du-bordeaux/index.html"

class LaMaisonDuBordeauxAproposView(TemplateView):
    template_name = "portfolio/la-maison-du-bordeaux/about.html"

class LaMaisonDuBordeauxProduitsView(TemplateView):
    template_name = "portfolio/la-maison-du-bordeaux/products.html"

class LaMaisonDuBordeauxBoutiqueView(TemplateView):
    template_name = "portfolio/la-maison-du-bordeaux/store.html"

class SunAndSurfView(TemplateView):
    template_name = "portfolio/sun-and-surf/index.html"

class DeMiTierraView(TemplateView):
    template_name = "portfolio/de-mi-tierra/index.html"

class LaFortunaTripView(TemplateView):
    template_name = "portfolio/la-fortuna-trip/index.html"

class DeMiTierrapView(TemplateView):
    template_name = "portfolio/de-mi-tierra/index.html"


class Error404View(TemplateView):
    template_name = "home/error-404.html"

def custom_404(request, exception):
    return render(request, 'home/erro-404.html', status=404)







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


from .utils.email_brevo import enviar_email_brevo  # asegúrate de tener esta línea

def formulario_contactar(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        company = request.POST.get("company", "")
        message = request.POST.get("message", "")

        asunto = f"Nuevo mensaje de contacto de {name}"
        contenido_html = f"""
        <h3>Nuevo mensaje desde el formulario</h3>
        <p><strong>Nombre:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Teléfono:</strong> {phone}</p>
        <p><strong>Empresa:</strong> {company}</p>
        <p><strong>Mensaje:</strong><br>{message}</p>
        """

        resultado = enviar_email_brevo(
            asunto=asunto,
            contenido_html=contenido_html,
            destinatario_email="info@euskodev.eus",
            destinatario_nombre="Euskodev"
        )

        if resultado:
            messages.success(request, "Mensaje enviado con éxito.")
        else:
            messages.error(request, "Error al enviar el mensaje.")

        return redirect("home_app:home")

    return redirect("home_app:home")

def formulario_contactar2(request):
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
        asunto = f"Euskodev Nuevo mensaje de contacto de {name}"
        contenido = (
            f"Nombre: {name}\n"
            f"Email: {email}\n"
            f"Teléfono: {phone}\n"
            f"Mensaje:\n{message}"
        )

        try:
            print("Try de la función send_mail")
            send_mail(
            asunto,
            contenido,
            settings.DEFAULT_FROM_EMAIL,
            ["info@euskodev.eus"],  # <-- cámbialo por otro correo real tuyo
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


def custom_404(request, exception):
    return render(request, 'home/404.html', status=404)


#estas seran las vsistas para los servicios que ofrecemos es decir para separar los servicios
#para nppoder poner mas informacion y no hacer mas lenta la pagina principal


def desarrollo_web(request):
    return render(request, 'home/desarrollo_web.html')

def reservas_y_pagos(request):
    return render(request, 'home/reservas_y_pagos.html')

def software_a_medida(request):
    return render(request, 'home/software_a_medida.html')

def inteligencia_artificial(request):
    return render(request, 'home/inteligencia_artificial.html')

def aplicaciones_moviles(request):
    return render(request, 'home/aplicaciones_moviles.html')

def sistema_ticket(request):
    return render(request, 'home/sistema_ticket.html')
    

def base(request):
    return render(request, 'home/base.html')
    


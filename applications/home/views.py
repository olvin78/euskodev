from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView
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

from .forms import JobApplicationForm
from django.urls import reverse_lazy


from .utils.email_api import enviar_email_brevo_api as enviar_email_brevo
import os
import base64

def formulario_contactar(request):
    if request.method == "POST":
        # Validación de reCAPTCHA
        if settings.RECAPTCHA_VERIFY_REQUESTS:
            recaptcha_response = request.POST.get("g-recaptcha-response")
            if not recaptcha_response:
                messages.error(request, "Por favor, completa la validación de reCAPTCHA.")
                return redirect("home_app:home")

            recaptcha_secret = getattr(settings, "RECAPTCHA_PRIVATE_KEY", "")
            if not recaptcha_secret:
                print("❌ Error: RECAPTCHA_PRIVATE_KEY no está configurado.")
                messages.error(request, "No se pudo validar reCAPTCHA. Inténtalo de nuevo.")
                return redirect("home_app:home")

            data = {
                'secret': recaptcha_secret,
                'response': recaptcha_response
            }

            try:
                r = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data=data,
                    timeout=6
                )
                result = r.json()
            except requests.RequestException as e:
                print(f"❌ Error al validar reCAPTCHA: {type(e).__name__}: {e}")
                messages.error(request, "No se pudo validar reCAPTCHA. Inténtalo de nuevo.")
                return redirect("home_app:home")

            if not result.get('success'):
                messages.error(request, "Error en la validación de reCAPTCHA. Inténtalo de nuevo.")
                return redirect("home_app:home")

        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        company = request.POST.get("company", "")
        message = request.POST.get("message", "")

        asunto = f"Mensaje desde la página principal de Euskodev - {name}"
        contenido_html = f"""
        <h3>Nuevo mensaje desde el formulario</h3>
        <p><strong>Nombre:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Teléfono:</strong> {phone}</p>
        <p><strong>Empresa:</strong> {company}</p>
        <p><strong>Mensaje:</strong><br>{message}</p>
        """

        destinatarios = getattr(settings, "CONTACT_RECIPIENTS", ["info@euskodev.eus", "euskodev@gmail.com"])
        
        exito_total = True
        for dest in destinatarios:
            resultado = enviar_email_brevo(
                asunto=asunto,
                contenido_html=contenido_html,
                destinatario_email=dest,
                destinatario_nombre="Euskodev"
            )
            if resultado:
                print(f"✅ Email enviado con éxito a {dest}")
            else:
                print(f"❌ Error al enviar email a {dest}")
                exito_total = False

        if exito_total:
            messages.success(request, "Mensaje enviado con éxito.")
        else:
            messages.warning(request, "El mensaje se envió, pero hubo problemas con algún destinatario.")

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
        return Blog.objects.order_by('-id')[:6]


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
    


class TrabajaConNosotrosView(TemplateView):
    template_name = 'home/trabaja_con_nosotros.html'







class EnviarSolicitudView(FormView):
    template_name = 'jobs/trabaja_con_nosotros_form.html'
    form_class = JobApplicationForm
    success_url = reverse_lazy('home_app:trabaja_gracias')

    def form_valid(self, form):
        print("✅ Entró en form_valid")  # ← Verifica que entra

        nombre = form.cleaned_data['nombre']
        apellido = form.cleaned_data['apellido']
        correo = form.cleaned_data['correo']
        puesto = form.cleaned_data['puesto']

        mensaje_usuario = form.cleaned_data.get('mensaje', '')

        mensaje_html = (
            f"Nuevo mensaje de solicitud de empleo:<br><br>"
            f"<strong>Nombre:</strong> {nombre} {apellido}<br>"
            f"<strong>Correo:</strong> {correo}<br>"
            f"<strong>Puesto:</strong> {puesto}<br><br>"
            f"<strong>Comentarios del candidato:</strong><br>{mensaje_usuario}"
        )

        destinatarios = getattr(settings, "CONTACT_RECIPIENTS", ["info@euskodev.eus", "euskodev@gmail.com"])
        
        cv_file = form.cleaned_data['curriculum']
        try:
            cv_content = cv_file.read()
            cv_encoded = base64.b64encode(cv_content).decode('utf-8')
            adjuntos = [{
                "content": cv_encoded,
                "name": cv_file.name
            }]
        except Exception as e:
            print(f"❌ Error al procesar el CV: {e}")
            adjuntos = None

        asunto = f"Nuevo candidato a Euskodev - {nombre} {apellido} - {puesto}"
        html_mensaje = f"""
        <h3>Nueva solicitud de empleo</h3>
        <p><strong>Nombre:</strong> {nombre} {apellido}</p>
        <p><strong>Email:</strong> {correo}</p>
        <p><strong>Puesto:</strong> {puesto}</p>
        <p><strong>Comentarios:</strong> {mensaje_usuario}</p>
        <p>Se adjunta el currículum en este correo.</p>
        """

        exito_total = True
        for dest in destinatarios:
            resultado = enviar_email_brevo(
                asunto=asunto,
                contenido_html=html_mensaje,
                destinatario_email=dest,
                destinatario_nombre="Admin Euskodev",
                adjuntos=adjuntos
            )
            if resultado:
                print(f"✅ Email de solicitud enviado con éxito a {dest}")
            else:
                print(f"❌ Error al enviar email de solicitud a {dest}")
                exito_total = False

        print(f"📨 Resultado del envío: {resultado}")  # ← Verifica que se envió (debe ser 1)

        return super().form_valid(form)

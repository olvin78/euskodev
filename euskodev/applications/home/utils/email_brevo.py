from django.core.mail import send_mail
from django.conf import settings
import socket

def enviar_email_brevo(asunto, contenido_html, destinatario_email, destinatario_nombre=""):
    try:
        print(f"DEBUG: Intentando enviar email a {destinatario_email} via SMTP {settings.EMAIL_HOST}:{settings.EMAIL_PORT}...")
        result = send_mail(
            subject=asunto,
            message=contenido_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinatario_email],
            html_message=contenido_html,
            fail_silently=False
        )
        print(f"DEBUG: Resultado de send_mail: {result}")
        return result
    except socket.timeout:
        print("❌ Error: Tiempo de espera agotado al conectar con el servidor de correo.")
        return None
    except Exception as e:
        print(f"❌ Error detallado al enviar email: {type(e).__name__}: {e}")
        return None

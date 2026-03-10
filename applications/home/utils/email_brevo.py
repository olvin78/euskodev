from django.core.mail import send_mail
from django.conf import settings

def enviar_email_brevo(asunto, contenido_html, destinatario_email, destinatario_nombre=""):
    try:
        result = send_mail(
            subject=asunto,
            message=contenido_html,  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinatario_email],
            html_message=contenido_html,  # HTML content
            fail_silently=False
        )
        return result
    except Exception as e:
        print("❌ Error al enviar email:", e)
        return None

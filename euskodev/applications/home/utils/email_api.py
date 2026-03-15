import requests
import base64
from django.conf import settings

def enviar_email_brevo_api(asunto, contenido_html, destinatario_email, destinatario_nombre="", adjuntos=None):
    """
    Envía un email usando la API de Brevo (HTTP).
    Soporta una lista de adjuntos: [{"content": b64_string, "name": "file.pdf"}]
    """
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": settings.BREVO_API_KEY
    }
    
    payload = {
        "sender": {
            "name": "Euskodev",
            "email": "euskodev@gmail.com"
        },
        "to": [
            {
                "email": destinatario_email,
                "name": destinatario_nombre or "Admin"
            }
        ],
        "subject": asunto,
        "htmlContent": contenido_html
    }
    
    if adjuntos:
        payload["attachment"] = adjuntos
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 201:
            print(f"✅ Email enviado con éxito vía API a {destinatario_email}")
            return True
        else:
            print(f"❌ Error de API Brevo ({response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión con la API de Brevo: {e}")
        return False

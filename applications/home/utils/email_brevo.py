from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import Configuration, ApiClient
from sib_api_v3_sdk.api import TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail
from django.conf import settings


def enviar_email_brevo(asunto, contenido_html, destinatario_email, destinatario_nombre=""):
    try:
        configuration = Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY

        api_instance = TransactionalEmailsApi(ApiClient(configuration))

        email = SendSmtpEmail(
            to=[{"email": destinatario_email, "name": destinatario_nombre}],
            sender={"email": settings.DEFAULT_FROM_EMAIL, "name": "Euskodev"},
            subject=asunto,
            html_content=contenido_html
        )

        response = api_instance.send_transac_email(email)
        return response

    except ApiException as e:
        print("❌ Error al enviar email con Brevo:", e)
        return None

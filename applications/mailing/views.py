from django.shortcuts import render
from .forms import MailingForm
from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def mailing_view(request):
    error = None
    sent = False

    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = [email.strip() for email in form.cleaned_data['recipients'].split(',')]

            try:
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key['api-key'] = settings.BREVO_API_KEY  # Asegúrate de tener esto en tu settings.py

                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                    sib_api_v3_sdk.ApiClient(configuration)
                )

                send_email = sib_api_v3_sdk.SendSmtpEmail(
                    subject=subject,
                    html_content=f"<html><body>{message}</body></html>",
                    sender={"name": "Euskodev", "email": "info@euskodev.eus"},
                    to=[{"email": email} for email in recipients],
                )

                api_instance.send_transac_email(send_email)
                sent = True

            except ApiException as e:
                error = f"❌ Error al enviar el mailing: {e}"

    else:
        form = MailingForm()

    return render(request, 'mailing/mailing.html', {
        'form': form,
        'sent': sent,
        'error': error,
    })

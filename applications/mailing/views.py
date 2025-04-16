from django.core.mail import get_connection, EmailMessage
from django.shortcuts import render
from .forms import MailingForm

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
                connection = get_connection()  # usa la configuración global SMTP
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email='info@euskodev.eus',  # asegúrate de que está verificado en Brevo
                    to=recipients,
                    connection=connection,
                )
                email.send()
                sent = True

            except Exception as e:
                error = str(e)  # Muestra el error real en la plantilla

    else:
        form = MailingForm()

    return render(request, 'mailing/manual_mailing.html', {
        'form': form,
        'sent': sent,
        'error': error,
    })

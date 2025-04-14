# mailing/views.py
from django.core.mail import send_mail, get_connection
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import MailingForm

def mailing_view(request):
    if request.method == "POST":
        form = MailingForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            raw_emails = form.cleaned_data['recipients']
            recipients = [e.strip() for e in raw_emails.split(',') if e.strip()]

            try:
                connection = get_connection()
                for i in range(0, len(recipients), 50):
                    batch = recipients[i:i + 50]
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        batch,
                        connection=connection,
                        fail_silently=False
                    )
                return redirect('dashboard_app:home')  # ✅ redirección al dashboard
            except Exception as e:
                return render(request, "mailing/manual_mailing.html", {
                    "form": form,
                    "error": f"{type(e).__name__}: {str(e)}"
                })
    else:
        form = MailingForm()

    return render(request, "mailing/manual_mailing.html", {
        "form": form
    })

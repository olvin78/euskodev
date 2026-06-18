# mailing/forms.py
from django import forms

class MailingForm(forms.Form):
    subject = forms.CharField(
        label="Asunto",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    recipients = forms.CharField(
        label="Destinatarios",
        help_text="Introduce los correos separados por coma",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

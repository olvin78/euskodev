from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)  # Aquí se agrega el reCAPTCHA






class JobApplicationForm(forms.Form):
    PUESTOS_CHOICES = [
        ('', 'Selecciona un puesto / Aukeratu postu bat'),

        # Desarrollo y tecnología
        ('desarrollador_web', 'Desarrollador Web / Web garatzailea'),
        ('backend', 'Desarrollador Backend / Backend garatzailea'),
        ('frontend', 'Desarrollador Frontend / Frontend garatzailea'),
        ('fullstack', 'Desarrollador Full Stack / Full Stack garatzailea'),
        ('devops', 'DevOps / DevOps ingeniaria'),

        # Diseño y contenido
        ('uiux', 'Diseñador UI/UX / UI/UX diseinatzailea'),
        ('grafico', 'Diseñador Gráfico / Diseinu grafikoa'),
        ('copywriter', 'Copywriter / Eduki sortzailea'),

        # Marketing y SEO
        ('seo', 'Especialista en SEO / SEO espezialista'),
        ('marketing_digital', 'Marketing Digital / Marketin digitala'),
        ('social_media', 'Gestor de Redes Sociales / Sare sozialetako arduraduna'),

        # Comercial y atención
        ('comercial', 'Comercial / Komertziala'),
        ('atencion_cliente', 'Atención al Cliente / Bezeroarentzako arreta'),

        # Administración y soporte
        ('administrativo', 'Administrativo / Administraria'),
        ('project_manager', 'Project Manager / Proiektu kudeatzailea'),
        ('soporte_tecnico', 'Soporte Técnico / Laguntza teknikoa'),
    ]

    nombre = forms.CharField(
        label='Nombre / Izena',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Jon / Adib: Jon'
        })
    )

    apellido = forms.CharField(
        label='Apellido / Abizena',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Etxebarria / Adib: Etxebarria'
        })
    )

    correo = forms.EmailField(
        label='Correo electrónico / Posta elektronikoa',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )

    puesto = forms.ChoiceField(
        label='Puesto / Postua',
        choices=PUESTOS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    curriculum = forms.FileField(
        label='Adjuntar currículum / Erantsi zure curriculum-a',
        widget=forms.ClearableFileInput(attrs={
            'class': 'd-none',
            'id': 'curriculum',
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        })
    )

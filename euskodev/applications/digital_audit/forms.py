from django import forms
from .models import DigitalizationAssessment

class DigitalizationAssessmentForm(forms.ModelForm):
    class Meta:
        model = DigitalizationAssessment
        fields = '__all__'
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'business_activity': forms.Textarea(attrs={'class': 'form-control','rows': 6,'placeholder': 'Describe brevemente a qué se dedica tu empresa'}),
        }

        # Aplicar Select a todos los booleanos con 3 estados
        widgets.update({
            field.name: forms.Select(attrs={'class': 'form-select'})
            for field in model._meta.fields
            if isinstance(field, (forms.fields.NullBooleanField,)) or (getattr(field, 'choices', None) and field.choices)
        })

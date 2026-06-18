from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'second_name', 'last_name', 'second_last_name', 
                  'phone', 'secondary_phone', 'email', 'company', 'position', 
                  'address', 'city', 'state', 'country', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

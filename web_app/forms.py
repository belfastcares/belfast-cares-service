from django import forms
from web_app.models import ContactResponse

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactResponse
        fields = ['name', 'email', 'phone', 'message']
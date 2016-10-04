from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=300)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)
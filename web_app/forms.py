from django import forms
from web_app.models import ContactResponse, Organisation, Wishlist, Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'county', 'postcode']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactResponse
        fields = ['name', 'email', 'phone', 'message']


class OrganisationAdminForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ['name', 'image', 'primary_contact', 'address', 'description', 'just_giving_link', 'raised', 'goal']


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['organisation', 'start_time', 'end_time', 'reoccurring', 'items']

    def clean(self):
        super(WishlistForm, self).clean()
        start_date = self.cleaned_data.get('start_time')
        end_date = self.cleaned_data.get('end_time')
        if (start_date and end_date) and (start_date > end_date):
            raise forms.ValidationError({'end_time': ["End time cannot come before start time."]})
        return self.cleaned_data

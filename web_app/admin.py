from django.contrib import admin

# Register your models here.
from django import forms

from .models import *

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = '__all__'

    def clean(self):
        start_date = self.cleaned_data.get('start_time')
        end_date = self.cleaned_data.get('end_time')
        if start_date > end_date:
            raise forms.ValidationError("End time cannot come before start time.")
        return self.cleaned_data


class WishlistAdmin(admin.ModelAdmin):
    form = WishlistForm
    filter_horizontal = ('items',)


class OrganisationAdmin(admin.ModelAdmin):
    fields = ('name', ('image', 'image_preview_large'), 'primary_contact', 'address', 'description', 'wishlist',
              'just_giving_link', ('raised', 'goal'))
    readonly_fields = ('image_preview_large',)
    list_display = ['name', 'image_preview_small', 'primary_contact', 'address', 'description', 'wishlist', 'just_giving_link', 'raised', 'goal']


admin.site.register(User)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Contact)
admin.site.register(Address)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Item)
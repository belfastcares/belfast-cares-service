from django.contrib import admin

# Register your models here.
from django import forms
from .models import *

# Customise default admin
admin.AdminSite.site_header = "Belfast Cares Administration"
admin.AdminSite.site_title = "Belfast Cares Site Admin"


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = '__all__'

    def clean(self):
        super(WishlistForm, self).clean()
        start_date = self.cleaned_data.get('start_time')
        end_date = self.cleaned_data.get('end_time')
        if start_date > end_date:
            raise forms.ValidationError("End time cannot come before start time.")
        return self.cleaned_data


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'

    def clean(self):
        super(OrganisationForm, self).clean()
        raised = self.cleaned_data.get('raised')
        goal = self.cleaned_data.get('goal')
        if raised < 0 or goal < 0:
            raise forms.ValidationError("Raised or goal cannot be less than 0.")
        return self.cleaned_data


class WishlistAdmin(admin.ModelAdmin):
    form = WishlistForm
    filter_horizontal = ('items',)


class OrganisationUserInline(admin.StackedInline):
    model = OrganisationUser
    extra = 1


class WishlistInline(admin.StackedInline):
    form = WishlistForm
    model = Wishlist
    filter_horizontal = ('items',)
    verbose_name_plural = 'Wishlist'


class OrganisationAdmin(admin.ModelAdmin):
    form = OrganisationForm
    fieldsets = (
        ('Basic Details', {
            'fields': ('name', ('image', 'image_preview_large'), 'description', 'primary_contact', 'address')
        }),
        ('Fund Raising Details', {
            'fields': ('just_giving_link', ('raised', 'goal'))
        })
    )

    list_display = ('image_preview_small', 'name', 'primary_contact', 'wishlist', 'address',
                    'just_giving_link', 'raised', 'goal', 'associated_user_accounts')
    list_display_links = ('image_preview_small', 'name')
    inlines = [OrganisationUserInline, WishlistInline]
    readonly_fields = ('image_preview_large',)
    search_fields = ['name']


class ContactResponseAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'name', 'email', 'phone', 'message')


admin.site.register(Volunteer)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Contact)
admin.site.register(Address)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Item)
admin.site.register(OrganisationUser)
admin.site.register(ContactResponse, ContactResponseAdmin)
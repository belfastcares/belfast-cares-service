from django.contrib import admin

from web_app.forms import AdminWishlistForm, OrganisationAdminForm
from .models import *

# Customise default admin
admin.AdminSite.site_header = "Belfast Cares Administration"
admin.AdminSite.site_title = "Belfast Cares Site Admin"


class WishlistAdmin(admin.ModelAdmin):
    form = AdminWishlistForm
    filter_horizontal = ('items',)


class OrganisationUserInline(admin.StackedInline):
    model = OrganisationUser
    extra = 1


class WishlistInline(admin.StackedInline):
    form = AdminWishlistForm
    model = Wishlist
    filter_horizontal = ('items',)
    verbose_name_plural = 'Wishlist'


class OrganisationAdmin(admin.ModelAdmin):
    form = OrganisationAdminForm
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

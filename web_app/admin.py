from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Contact)
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(Item)
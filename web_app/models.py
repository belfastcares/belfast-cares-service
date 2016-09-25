from __future__ import unicode_literals

import os
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Address(models.Model):
    address_line = models.CharField('address_line', max_length=100)
    county = models.CharField('country', max_length=50)
    postcode = models.CharField('postcode', max_length=10)

    def __str__(self):
        return self.address_line + " " + self.county


@python_2_unicode_compatible
class Contact(models.Model):
    first_name = models.CharField('first_name', max_length=30)
    surname = models.CharField('surname', max_length=30)
    telephone = models.CharField('telephone', max_length=15)
    mobile = models.CharField('mobile', max_length=15)
    email = models.EmailField('email', max_length=50)
    description = models.TextField('description')
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.surname

@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField('name', max_length=50)
    description = models.TextField('description')

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Wishlist(models.Model):
    start_time = models.DateTimeField('start_time')
    end_time = models.DateTimeField('end_time')
    reoccurring = models.BooleanField('reoccurring')
    items = models.ManyToManyField(Item)

    def __str__(self):
        return "wishlist " + str(self.id)

def get_logo_file_name(instance, filename):
    return os.path.join('uploads', instance.name, 'logo' + os.path.splitext(filename)[1])

@python_2_unicode_compatible
class Organisation(models.Model):
    name = models.CharField('name', max_length=30)
    image = models.ImageField(upload_to=get_logo_file_name, blank=True)
    primary_contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    description = models.TextField('description')
    wishlist = models.OneToOneField(Wishlist, on_delete=models.CASCADE)
    just_giving_link = models.URLField('just giving link', max_length=255, blank=True)
    raised = models.DecimalField('raised', max_digits=25, decimal_places=2, blank=True)
    goal = models.DecimalField('goal', max_digits=25, decimal_places=2, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.name)

    def image_preview_large(self):
        if self.image:
            return '<img src="%s" width="150" height="150"/>' % self.image.url
        else:
            return 'No Logo'
    image_preview_large.allow_tags = True
    image_preview_large.short_description = 'Logo Preview'

    def image_preview_small(self):
        if self.image:
            return '<img src="%s" width="50" height="50"/>' % self.image.url
        else:
            return 'No Logo'
    image_preview_small.allow_tags = True
    image_preview_small.short_description = 'Image Preview'

@python_2_unicode_compatible
class User(models.Model):
    username = models.CharField('username', unique=True, max_length=80)
    password = models.CharField('password', max_length=100)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
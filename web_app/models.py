from __future__ import unicode_literals

import os, re
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.utils.html import format_html


@python_2_unicode_compatible
class Address(models.Model):
    address_line = models.CharField('address line', max_length=100)
    county = models.CharField('country', max_length=50)
    postcode = models.CharField('postcode', max_length=10)

    def __str__(self):
        return self.address_line + " " + self.county


@python_2_unicode_compatible
class Contact(models.Model):
    first_name = models.CharField('first name', max_length=30)
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

def get_logo_file_name(instance, filename):
    org_name = re.sub('[^0-9a-zA-Z]+','', instance.name)
    return os.path.join('uploads', org_name, 'logo' + os.path.splitext(filename)[1])


@python_2_unicode_compatible
class Organisation(models.Model):
    name = models.CharField('name', max_length=30)
    image = models.ImageField(upload_to=get_logo_file_name, blank=True, default='default.jpg')
    primary_contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    description = models.TextField('description')
    just_giving_link = models.URLField('just giving link', max_length=255, blank=True)
    raised = models.DecimalField('raised', max_digits=25, decimal_places=2, blank=True)
    goal = models.DecimalField('goal', max_digits=25, decimal_places=2, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.name


    def image_preview_large(self):
        if self.image:
            return format_html(
                '<img src="{}" width="150" height="150"/>',
                self.image.url
            )
        else:
            return 'No Logo'
    image_preview_large.short_description = 'Image Preview'

    def image_preview_small(self):
        if self.image:
            return format_html(
                '<img src="{}" width="50" height="50"/>',
                self.image.url
            )
        else:
            return 'No Logo'
    image_preview_small.short_description = 'Image Preview'

    def associated_user_accounts(self):
        return ','.join(str(item.user.id) +': ' + item.user.username for item in self.organisationuser_set.all())
    associated_user_accounts.short_description = 'User Accounts'

    def percentage_to_fund_raising_goal(self):
        val = int(round(self.raised / self.goal * 100))
        if val > 100:
            return 100
        return val

@python_2_unicode_compatible
class Wishlist(models.Model):
    organisation = models.OneToOneField(Organisation, on_delete=models.CASCADE)
    start_time = models.DateTimeField('start_time')
    end_time = models.DateTimeField('end_time')
    reoccurring = models.BooleanField('reoccurring')
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.organisation.name + " Wishlist"

@python_2_unicode_compatible
class OrganisationUser(models.Model):
    user = models.OneToOneField(User, verbose_name="User account details")
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, verbose_name='Contact details')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.organisation.name + " Organisation User " + str(self.user.username)
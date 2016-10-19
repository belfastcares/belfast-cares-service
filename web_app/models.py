from __future__ import unicode_literals

import os
import re
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@python_2_unicode_compatible
class Address(models.Model):
    address_line = models.CharField('address line', max_length=100)
    county = models.CharField('county', max_length=50)
    postcode = models.CharField('postcode', max_length=10)

    def __str__(self):
        return self.address_line + " " + self.county


@python_2_unicode_compatible
class Contact(models.Model):
    first_name = models.CharField('first name', max_length=30)
    surname = models.CharField('surname', max_length=30)
    telephone = models.CharField('telephone', max_length=15, blank=True)
    mobile = models.CharField('mobile', max_length=15, blank=True)
    email = models.EmailField('email', max_length=50)
    description = models.TextField('description', blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.surname


@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField('name', max_length=50)
    description = models.TextField('description')

    def __str__(self):
        return self.name

def get_volunteer_profile_picture_path(instance, filename):
    sanitized_volunteer_f_name = re.sub('[^0-9a-zA-Z]+', '', instance.first_name)
    sanitized_volunteer_s_name = re.sub('[^0-9a-zA-Z]+', '', instance.surname)

    return os.path.join('uploads', 'volunteers', 'profile_' + str(instance.id)+ "_" + sanitized_volunteer_f_name + '_'
                        + sanitized_volunteer_s_name + os.path.splitext(filename)[1])

def get_organisation_logo_path(instance, filename):
    sanitized_org_name = re.sub('[^0-9a-zA-Z]+', '', instance.name)

    return os.path.join('uploads', 'organisations', 'organisation_' + str(instance.id) + '_' + sanitized_org_name +
                        os.path.splitext(filename)[1])

class Volunteer(models.Model):
    first_name = models.CharField('first_name', max_length=30)
    surname = models.CharField('surname', max_length=30)
    occupation = models.CharField('occupation', max_length=30)
    about_me = models.CharField('about_me', max_length=300)
    image = models.ImageField(upload_to=get_volunteer_profile_picture_path, blank=True, default='default.jpg')
    experience = models.CharField('experience', max_length=300)
    training = models.CharField('training', max_length=100)
    facebook_link = models.URLField('facebook_link', max_length=255, blank=True)
    twitter_link = models.URLField('twitter_link', max_length=255, blank=True)
    email = models.EmailField('email', max_length=50, blank=False)
    public = models.BooleanField('public', default=False)

    def __str__(self):
        return self.first_name + ' ' + self.surname


@python_2_unicode_compatible
class Organisation(models.Model):
    name = models.CharField('name', max_length=30)
    image = models.ImageField(upload_to=get_organisation_logo_path, blank=True, default='default.jpg')
    primary_contact = ForeignKey(Contact, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    description = models.TextField('description')
    just_giving_link = models.URLField('just giving link', max_length=255, blank=True)
    raised = models.DecimalField('raised', max_digits=25, decimal_places=2, blank=True, null=True)
    goal = models.DecimalField('goal', max_digits=25, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " " + self.name

    def image_preview_large(self):
        if self.image:
            return format_html(
                '<img src="{}" width="150" height="150"/>',
                self.image.url
            )
        return 'No Logo'

    image_preview_large.short_description = 'Image Preview'

    def image_preview_small(self):
        if self.image:
            return format_html(
                '<img src="{}" width="50" height="50"/>',
                self.image.url
            )
        return 'No Logo'

    image_preview_small.short_description = 'Image Preview'

    def associated_user_accounts(self):
        if not self.organisationuser_set.count():
            return 'No Accounts'
        return ','.join(str(item.user.id) + ': ' + item.user.username for item in self.organisationuser_set.all())

    associated_user_accounts.short_description = 'User Accounts'

    def percentage_to_fund_raising_goal(self):
        if not (self.raised and self.goal):
            return 0
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
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='Contact details')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.organisation.name + " Organisation User " + str(self.user.username)


@python_2_unicode_compatible
class ContactResponse(models.Model):
    name = models.CharField('name', max_length=300)
    email = models.EmailField('email', max_length=50)
    phone = models.CharField('phone number', max_length=15, blank=True)
    message = models.TextField('message')
    timestamp = models.DateTimeField('timestamp', auto_now_add=True)

    def __str__(self):
        return str(self.id) + " " + self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

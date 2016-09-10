from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
@python_2_unicode_compatible
class Wishlist(models.Model):
    start_time = models.DateTimeField('start_time')
    end_time = models.DateTimeField('end_time')
    reoccurring = models.BooleanField('reoccurring')
    def __str__(self):
        return self.id

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
    email = models.CharField('email', max_length=50)
    description = models.TextField('description')
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    def __str__(self):
        return self.first_name + " " + self.surname

@python_2_unicode_compatible
class Organisation(models.Model):
    name = models.CharField('name', max_length=30)
    image_url = models.CharField('image_url', max_length=255)
    primary_contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    description = models.TextField('description')
    wishlist = models.OneToOneField(Wishlist, on_delete=models.CASCADE)
    def __str__(self):
        return self.id + " " + self.name


@python_2_unicode_compatible
class User(models.Model):
    username = models.CharField('username', unique=True, max_length=80)
    password = models.CharField('password', max_length=100)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    def __str__(self):
        return self.username

@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField('name', max_length=50)
    description = models.TextField('description')
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
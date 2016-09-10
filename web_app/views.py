from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def volunteer_listing(request):
    return render(request, 'volunteer_listing.html')

def volunteer_single(request, volunteer_id):
    return render(request, 'volunteer_single.html', {'id': volunteer_id})


def charities_listing(request):
    return render(request, 'charities_listing.html')


def charities_single(request, charity_id):
    organisation = Organisation.objects.filter(id=charity_id)[0]
    org_address = organisation.address
    org_wishlist = organisation.wishlist
    org_contact = organisation.primary_contact

    return render(request, 'charities_single.html', {'organisation': organisation,
                                                     'org_address': org_address,
                                                     'org_wishlist': org_wishlist,
                                                     'org_primary': org_contact})


def help(request):
    return render(request, 'help.html')


def contact(request):
    return render(request, 'contact.html')


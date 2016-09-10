from django.shortcuts import render, get_object_or_404

from .models import *


def index(request):
    charities = Organisation.objects.all()
    return render(request, 'index.html', {'charities': charities})


def login(request):
    return render(request, 'login.html')


def volunteer_single(request, volunteer_id):
    volunteer_data = ''
    return render(request, 'volunteer_single.html', {'id': volunteer_id})


def charities_listing(request):
    charities = Organisation.objects.all()
    return render(request, 'charities_listing.html', {'charities': charities})


def charities_single(request, charity_id):
    organisation = get_object_or_404(Organisation, id=charity_id)
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

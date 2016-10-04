from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import *


def index(request):
    organisations = Organisation.objects.all()
    return render(request, 'index.html', {'organisations': organisations})


def login(request):
    return render(request, 'login.html')


def volunteer_single(request, volunteer_id):
    volunteer_data = ''
    return render(request, 'volunteer_single.html', {'id': volunteer_id})


def organisation_listing(request):
    organisations = Organisation.objects.all()
    return render(request, 'organisation_listing.html', {'organisations': organisations})


def organisation_single(request, organisation_id):
    organisation = get_object_or_404(Organisation, id=organisation_id)
    org_address = organisation.address
    org_wishlist = organisation.wishlist
    org_contact = organisation.primary_contact

    return render(request, 'organisation_single.html', {'organisation': organisation,
                                                     'org_address': org_address,
                                                     'org_wishlist': org_wishlist,
                                                     'org_primary': org_contact})

@login_required(login_url='/login/')
def account_dashboard(request):
    return render(request, 'account_dashboard.html')


def help(request):
    return render(request, 'help.html')


def contact(request):
    return render(request, 'contact.html')

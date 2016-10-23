from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from web_app.forms import ContactForm, OrganisationRegistrationForm, ContactRegistrationForm, AddressForm
from .models import *


def index(request):
    organisations = Organisation.objects.all()
    return render(request, 'index.html', {'organisations': organisations})


def volunteer_single(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id, public=True)
    return render(request, 'volunteer_single.html', {'volunteer': volunteer})


def volunteer_listing(request):
    volunteers = Volunteer.objects.filter(public=True)
    return render(request, 'volunteer_listing.html', {'volunteers': volunteers})


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


def register_organisation(request):

    if request.method == "POST":
        org_form = OrganisationRegistrationForm(request.POST, prefix='org')
        org_addr_form = AddressForm(request.POST, prefix='org_addr')
        contact_form = ContactRegistrationForm(request.POST, prefix='cont')
        contact_addr_form = AddressForm(request.POST, prefix='cont_addr')
        # Make sure all forms are valid before continuing
        if all([org_form.is_valid(), org_addr_form.is_valid(), contact_form.is_valid(), contact_addr_form.is_valid()]):
            organisation = org_form.save(commit=False)
            organisation.address = org_addr_form.save()

            organisation_prim_cont = contact_form.save(commit=False)
            organisation_prim_cont.address = contact_addr_form.save()
            organisation_prim_cont.save()

            organisation.primary_contact = organisation_prim_cont
            organisation.save()
            messages.success(request, 'Organisation added successfully.')
            return HttpResponseRedirect(reverse('register_organisation'))
    else:
        org_form = OrganisationRegistrationForm(prefix='org')
        org_addr_form = AddressForm(prefix='org_addr')
        contact_form = ContactRegistrationForm(prefix='cont')
        contact_addr_form = AddressForm(prefix='cont_addr')
    return render(request, 'registration/register_organisation.html', {'org_form': org_form,
                                                                       'org_addr_form': org_addr_form,
                                                                       'contact_form': contact_form,
                                                                       'contact_addr_form': contact_addr_form})


def register_volunteer(request):
    pass


@login_required(login_url='/login/')
def account_dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:index'))
    return render(request, 'account_dashboard.html')


def help(request):
    return render(request, 'help.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for getting in touch. Someone will be in contact shortly.')
            return HttpResponseRedirect(reverse(contact))
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

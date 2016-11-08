from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db import transaction, DatabaseError
from django.forms import modelform_factory, modelformset_factory
from django.forms.widgets import CheckboxSelectMultiple
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from formtools_addons import NamedUrlSessionMultipleFormWizardView
from web_app.forms import ContactForm, AddressForm, WishlistForm
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


register_organisation_form_list = [
    ("organisation_info", (
        ('org_details', modelform_factory(Organisation, fields=('name', 'image', 'description', 'just_giving_link',
                                                                'raised', 'goal',))),
        ('org_address', AddressForm),
    )),
    ("primary_contact_info", (
        ('primary_contact_details',
         modelform_factory(Contact, fields=('first_name', 'surname', 'telephone', 'mobile',
                                            'email', 'description'))),
        ('primary_contact_address', AddressForm)
    )),
    ('organisation_accounts', (
        ('org_user_login', UserCreationForm),

        ('org_user_contact', modelform_factory(Contact, fields=('first_name', 'surname', 'telephone', 'mobile',
                                                                'email', 'description'))),
        ('org_user_address', AddressForm)

    )),
    ('wishlist_info', (
        ('wishlist_details', modelform_factory(Wishlist, WishlistForm, fields=('start_time', 'end_time', 'reoccurring',
                                                                               'items'),
                                               widgets={'items': CheckboxSelectMultiple()})),
        ('extra_item_details', modelformset_factory(Item, fields=('name', 'description'), extra=3, can_delete=False,
                                                    max_num=3, validate_max=True))
    ))
]


class RegisterOrganisationWizard(NamedUrlSessionMultipleFormWizardView):
    templates = {
        "organisation_info": 'registration/organisation/register_organisation_step_1.html',
        "primary_contact_info": 'registration/organisation/register_organisation_step_2.html',
        "organisation_accounts": 'registration/organisation/register_organisation_step_3.html',
        "wishlist_info": 'registration/organisation/register_organisation_step_4.html'
    }

    def get_context_data(self, forms, **kwargs):
        context = super(RegisterOrganisationWizard, self).get_context_data(forms=forms, **kwargs)
        return context

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    file_storage = FileSystemStorage()

    def done(self, form_dict, **kwargs):
        # Execute the following in a db transaction, if anything fails rollback the db so we are not left with
        # incomplete data
        try:
            with transaction.atomic():
                # process primary contact
                primary_contact = form_dict['primary_contact_info']['primary_contact_details'].save(commit=False)
                primary_contact.address = form_dict['primary_contact_info']['primary_contact_address'].save()
                primary_contact.save()

                # process organisation
                new_organisation = form_dict['organisation_info']['org_details'].save(commit=False)
                new_organisation.address = form_dict['organisation_info']['org_address'].save()
                new_organisation.primary_contact = primary_contact
                new_organisation.save()

                # process organisation accounts
                org_user_contact = form_dict['organisation_accounts']['org_user_contact'].save(commit=False)
                org_user_contact.address = form_dict['organisation_accounts']['org_user_address'].save()
                org_user_contact.save()
                org_user_login = form_dict['organisation_accounts']['org_user_login'].save()

                OrganisationUser.objects.create(user=org_user_login, contact=org_user_contact,
                                                organisation=new_organisation)

                # process wishlist
                wishlist = form_dict['wishlist_info']['wishlist_details'].save(commit=False)
                wishlist.organisation = new_organisation
                wishlist.save()

                # when using commit=False, have to explicitly save many to many relationships
                form_dict['wishlist_info']['wishlist_details'].save_m2m()

                # process additional wishlist items
                new_items = form_dict['wishlist_info']['extra_item_details'].save()
                wishlist.items.add(*new_items)

        except DatabaseError:
            messages.error(self.request, "Something went wrong creating your organisation."
                                         "Please try again.")
            return HttpResponseRedirect(reverse("register_organisation_wizard"))

        messages.success(self.request, "Your organisation has been created.")

        return render(self.request, 'registration/organisation/register_organisation_complete.html',
                      {'organisation': new_organisation})


registration_organisation_wizard_view = RegisterOrganisationWizard.as_view(register_organisation_form_list,
                                                                           url_name="register_organisation_wizard_step",
                                                                           instance_dict={
                                                                               'wishlist_info': {
                                                                                   'extra_item_details':
                                                                                       Item.objects.none(),
                                                                               },
                                                                           })


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


def register(request):
    return render(request, 'register.html', {'register': []})

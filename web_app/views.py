from django.shortcuts import render, get_object_or_404
from web_app.models import Organisation

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
    organisation = get_object_or_404(Organisation, pk=charity_id)
    return render(request, 'charities_single.html', {'id': organisation.id})


def help(request):
    return render(request, 'help.html')


def contact(request):
    return render(request, 'contact.html')


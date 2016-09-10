from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def volunteer_listing(request):
    return render(request, 'volunteer_listing.html')

def volunteer_single(request, volunteer_id):
    volunteer_data = ''
    return render(request, 'volunteer_single.html', {'id': volunteer_id})


def charities_listing(request):
    return render(request, 'charities_single.html')


def charities_single(request, charity_id):
    return render(request, 'charities_single.html', {'id': charity_id})


def help(request):
    return render(request, 'help.html')


def contact(request):
    return render(request, 'contact.html')


from django.shortcuts import render
from web_app.models import Organisation

def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def volunteer_listing(request):
    return render(request, 'volunteer_listing.html')


def volunteer_single(request):
    return render(request, 'volunteer_single.html')


def charities_listing(request):
    charities = Organisation.objects.all()
    return render(request, 'charities_listing.html', {'charities': charities})


def charities_single(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'charities_single.html', {'id': post})


def help(request):
    return render(request, 'help.html')


def contact(request):
    return render(request, 'contact.html')

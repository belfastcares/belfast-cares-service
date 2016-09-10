from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def volunteer_listing(request):
    return render(request, 'volunteer_listing.html')


def volunteer_single(request):
    return render(request, 'volunteer_single.html')


def charities_listing(request):
    return render(request, 'charities_single.html')


def charities_single(request):
    return render(request, 'charities_single.html')


def help(request):
    return render(request, 'help.html')


def contact(request):
    return render(request, 'contact.html')

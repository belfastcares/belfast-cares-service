from django.contrib.auth.models import User
from rest_framework import viewsets
from web_app.models import Contact
from web_app.serializers import UserSerializer, ContactSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

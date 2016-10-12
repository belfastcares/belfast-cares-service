from rest_framework import viewsets
from web_app.pagination import StandardResultsSetPagination
from web_app.serializers import *


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContactViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class AddressViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ItemViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class OrganisationUserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = OrganisationUser.objects.all()
    serializer_class = OrganisationUserSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


class ContactResponseViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = ContactResponse.objects.all()
    serializer_class = ContactResponseSerializer


class VolunteerViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

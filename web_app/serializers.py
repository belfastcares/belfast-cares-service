from rest_framework import serializers
from web_app.models import *


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'surname', 'telephone', 'mobile', 'email', 'description', 'address')


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('address_line', 'county', 'postcode')


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'description')


class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('name', 'image', 'primary_contact', 'address', 'description', 'just_giving_link', 'raised', 'goal')


class OrganisationUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganisationUser
        fields = ('user', 'contact', 'organisation')


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('organisation', 'start_time', 'end_time', 'reoccurring', 'items')


class ContactResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContactResponse
        fields = ('name', 'email', 'phone', 'message', 'timestamp')


class VolunteerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Volunteer
        fields = ('first_name', 'surname', 'occupation', 'about_me', 'experience', 'training', 'facebook_link', 'twitter_link', 'email')

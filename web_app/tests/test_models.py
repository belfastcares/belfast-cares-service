import datetime

from unittest import mock

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import Storage
from django.test import TestCase
from django.utils import timezone
from web_app.models import Address, Contact, ContactResponse, Item, Organisation, OrganisationUser, Wishlist, Volunteer


class AddressModelTest(TestCase):
    def setUp(self):
        Address.objects.create(address_line="33 Test Street", county="Antrim", postcode="BT9 RGH")

    def test_should_fail_if_response_is_not_valid_match(self):
        address = Address.objects.get(address_line="33 Test Street")
        self.assertEqual(str(address), "33 Test Street Antrim", "Address string representation does not match expected")


class ContactModelTest(TestCase):
    def setUp(self):
        Address.objects.create(address_line="33 Test Street", county="Antrim", postcode="BT9 RGH")
        Contact.objects.create(first_name="Joe", surname="Bloggs", telephone="02890768976", mobile="07716453657",
                               email="j.bloggs@hotmail.com", description="A generic Test User",
                               address=Address.objects.get(address_line="33 Test Street"))

    def test_should_fail_if_response_is_not_valid_match(self):
        contact = Contact.objects.get(address__address_line="33 Test Street")
        self.assertEqual(str(contact), "Joe Bloggs", "Contact string representation does not match expected")


class ItemModelTest(TestCase):
    def setUp(self):
        Item.objects.create(name="Sleeping Bag", description="Warm, durable & waterproof if possible")

    def test_should_fail_if_response_is_not_valid_match(self):
        item = Item.objects.all()[0]
        self.assertEqual(str(item), "Sleeping Bag", "Item string representation does not match expected")


def create_organisation():
    Address.objects.create(address_line="33 Test Street", county="Antrim", postcode="BT9 RGH")
    Contact.objects.create(first_name="Joe", surname="Bloggs", telephone="02890768976", mobile="07716453657",
                           email="j.bloggs@hotmail.com", description="A generic Test User",
                           address=Address.objects.get(address_line="33 Test Street"))

    # It's considered best practice to avoid interaction with external services when testing, one example
    # being the file system. To work with the ImageField, mocking can be used to avoid file system interaction
    # as shown in this guide: https://joeray.me/mocking-files-and-file-storage-for-testing-django-models.html

    file_mock = mock.MagicMock(spec=File, name='FileMock')
    file_mock.name = 'test1.jpg'

    organisation = Organisation(name='St. Vincent de Paul', primary_contact=Contact.objects.all()[0],
                                image=file_mock,
                                address=Address.objects.all()[0],
                                description='No work of charity is foreign to the society. Our work through person '
                                            'to person contact encompasses every form of aid that alleviates '
                                            'suffering and promotes the dignity of mankind. The society strives not'
                                            ' only to alleviate need but also to discover and redress the '
                                            'situations which cause it. It services everyone in need, regardless of'
                                            ' creed, opinion,colour, origin or caste.',
                                just_giving_link='http://www.twitter.com', raised=60, goal=500)

    storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
    storage_mock.save = mock.MagicMock(name='save')
    storage_mock.save.return_value = '/tmp/test1.jpg'

    with mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock):
        # The asset is saved to the database but our mock storage
        # system is used so we don't touch the filesystem
        organisation.save()


class OrganisationModelTest(TestCase):
    def setUp(self):
        create_organisation()

    def test_should_fail_if_response_is_not_valid_match(self):
        organisation = Organisation.objects.all()[0]
        self.assertEqual(str(organisation), str(organisation.id) + " " + "St. Vincent de Paul",
                         "Organisation string representation does not match expected")

    def test_image_preview_large_valid_logo(self):
        organisation = Organisation.objects.all()[0]
        self.assertEqual(organisation.image_preview_large(), '<img src="/tmp/test1.jpg" width="150" height="150"/>',
                         "Generated html does not match expected")

    def test_image_preview_large_no_logo(self):
        organisation = Organisation.objects.all()[0]
        organisation.image = None
        self.assertEqual(organisation.image_preview_large(), 'No Logo',
                         "Response does not match expected")

    def test_image_preview_small_valid_logo(self):
        organisation = Organisation.objects.all()[0]
        self.assertEqual(organisation.image_preview_small(), '<img src="/tmp/test1.jpg" width="50" height="50"/>',
                         "Generated html does not match expected")

    def test_image_preview_small_no_logo(self):
        organisation = Organisation.objects.all()[0]
        organisation.image = None
        self.assertEqual(organisation.image_preview_small(), 'No Logo',
                         "Response does not match expected")

    def test_associated_user_accounts(self):
        organisation = Organisation.objects.all()[0]

        org_1 = OrganisationUser(user=User.objects.create_user(username='testuser1',
                                                               password='testpassword'),
                                 contact=Contact.objects.all()[0],
                                 organisation=Organisation.objects.all()[0])
        org_1.save()

        org_2 = OrganisationUser(user=User.objects.create_user(username='testuser2',
                                                               password='testpassword2'),
                                 contact=Contact.objects.all()[0],
                                 organisation=Organisation.objects.all()[0])
        org_2.save()

        self.assertEqual(organisation.associated_user_accounts(), str(org_1.id) + ": " + org_1.user.username + ","
                         + str(org_2.id) + ": " + org_2.user.username,
                         "Output from method does not match expected output")

    def test_percentage_to_fund_raising_goal(self):
        organisation = Organisation.objects.all()[0]
        self.assertEqual(organisation.percentage_to_fund_raising_goal(), 12, "Percentage calculated does not match"
                                                                             "expected")


class WishlistModelTest(TestCase):
    def setUp(self):
        create_organisation()
        Wishlist.objects.create(organisation=Organisation.objects.all()[0], start_time=timezone.now(),
                                end_time=timezone.now() + datetime.timedelta(days=30), reoccurring=False)

    def test_should_fail_if_response_is_not_valid_match(self):
        wishlist = Wishlist.objects.all()[0]
        self.assertEqual(str(wishlist), "St. Vincent de Paul Wishlist", "Wishlist string representation does not"
                                                                        "match expected")


class OrganisationUserTest(TestCase):
    def setUp(self):
        create_organisation()
        OrganisationUser.objects.create(user=User.objects.create_user(username='testuser1',
                                                                      password='testpassword1'),
                                        contact=Contact.objects.all()[0],
                                        organisation=Organisation.objects.all()[0])

    def test_should_fail_if_response_is_not_valid_match(self):
        org_user = OrganisationUser.objects.all()[0]
        self.assertEqual(str(org_user), "St. Vincent de Paul Organisation User testuser1",
                         "OrganisationUser string representation does not match expected")


class ContactResponseTest(TestCase):
    def setUp(self):
        ContactResponse.objects.create(name='Joe', email="joe@tester.com", phone="0289556786", message='Test message')

    def test_should_fail_if_response_is_not_valid_match(self):
        contact_response = ContactResponse.objects.all()[0]
        self.assertEqual(str(contact_response), str(contact_response.id) + " " +
                         contact_response.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                         "Contact response string representation does not match expected")


class VolunteerResponseTest(TestCase):
    def setUp(self):
        Volunteer.objects.create(name='Joe Bloggs', occupation='Volunteer', about_me='Working hard!',
                                 experience='Helping at a local youth center',
                                 training='No formal training', facebook_link='http://www.facebook.com/joeblogs',
                                 twitter_link='http://www.twitter.com/joebloggs', email='joe@bloggs.com')

    def test_should_fail_if_response_is_not_valid_match(self):
        volunteer = Volunteer.objects.all()[0]
        self.assertEqual(str(volunteer), 'Joe Bloggs')

from datetime import timedelta
from unittest import mock

from django.core.files import File
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from web_app.forms import ContactForm, OrganisationAdminForm, WishlistForm
from web_app.models import Contact, Address, Item, Organisation


class ContactFormTest(SimpleTestCase):

    def test_should_fail_if_form_deemed_invalid_with_valid_data(self):
        form = ContactForm({
            'name': 'Joe Tester',
            'email': 'joe@test.com',
            'phone': '07865476338',
            'message': 'This is a test message'
        })
        self.assertTrue(form.is_valid(), 'Form was deemed invalid with valid data')

    def test_should_fail_if_form_deemed_valid_with_blank_data(self):
        form = ContactForm({})
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 3, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['name'], ['This field is required.'], 'Error not raised for empty name field')
        self.assertEqual(form.errors['email'], ['This field is required.'], 'Error not raised for empty email field')
        self.assertEqual(form.errors['message'], ['This field is required.'],
                         'Error not raised for empty message field')

    def test_should_fail_if_form_deemed_valid_with_invalid_email(self):
        form = ContactForm({
            'name': 'Joe Tester',
            'email': 'joetest.com',
            'phone': '07865476338',
            'message': 'This is a test message'
        })
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 1, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'],
                         'Error not raised for invalid email field')


class OrganisationAdminFormTest(TestCase):

    def setUp(self):
        self.file_mock = mock.MagicMock(spec=File, name='File')
        self.file_mock.name = 'test1.jpg'
        Address.objects.create(address_line="33 Test Street", county="Antrim", postcode="BT9 RGH")
        Contact.objects.create(first_name="Joe", surname="Bloggs", telephone="02890768976", mobile="07716453657",
                               email="j.bloggs@hotmail.com", description="A generic Test User",
                               address=Address.objects.get(address_line="33 Test Street"))

    def test_should_fail_if_form_deemed_invalid_with_valid_data(self):
        form = OrganisationAdminForm({
            'name': 'Test Organisation',
            'image': self.file_mock,
            'primary_contact': Contact.objects.all()[0].pk,
            'address': Address.objects.all()[0].pk,
            'description': 'Test description',
            'just_giving_link': 'http://www.test.com',
            'raised': 50,
            'goal': 60
        })
        self.assertTrue(form.is_valid(), 'Form was deemed invalid with valid data')

    def test_should_fail_if_form_deemed_valid_with_blank_data(self):
        form = OrganisationAdminForm({})
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 4, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['name'], ['This field is required.'], 'Error not raised for empty name field')
        self.assertEqual(form.errors['primary_contact'], ['This field is required.'],
                         'Error not raised for empty primary contact field')
        self.assertEqual(form.errors['address'], ['This field is required.'],
                         'Error not raised for empty address field')
        self.assertEqual(form.errors['description'], ['This field is required.'],
                         'Error not raised for empty description field')

    def test_should_fail_if_form_deemed_valid_with_invalid_relational_data(self):
        form = OrganisationAdminForm({
            'name': 'Test Organisation',
            'image': self.file_mock,
            'primary_contact': 6,
            'address': 7,
            'description': 'Test description',
            'just_giving_link': 'http://www.test.com',
            'raised': 50,
            'goal': 60
        })
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 2, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['primary_contact'], ['Select a valid choice. '
                                                          'That choice is not one of the available choices.'],
                         'Error not raised for non-existent primary contact field')
        self.assertEqual(form.errors['address'], ['Select a valid choice. '
                                                  'That choice is not one of the available choices.'],
                         'Error not raised for non-existent address field')

    def test_should_fail_if_form_deemed_invalid_with_blank_raised(self):
        form = OrganisationAdminForm({
            'name': 'Test Organisation',
            'image': self.file_mock,
            'primary_contact': Contact.objects.all()[0].pk,
            'address': Address.objects.all()[0].pk,
            'description': 'Test description',
            'just_giving_link': 'http://www.test.com',
            'goal': 60
        })
        self.assertTrue(form.is_valid(), 'Form was deemed invalid with valid data')

    def test_should_fail_if_form_deemed_invalid_with_blank_goal(self):
        form = OrganisationAdminForm({
            'name': 'Test Organisation',
            'image': self.file_mock,
            'primary_contact': Contact.objects.all()[0].pk,
            'address': Address.objects.all()[0].pk,
            'description': 'Test description',
            'just_giving_link': 'http://www.test.com',
            'raised': 50,
        })
        self.assertTrue(form.is_valid(), 'Form was deemed invalid with valid data')

    def test_should_fail_if_form_deemed_valid_with_negative_raised(self):
        form = OrganisationAdminForm({
            'name': 'Test Organisation',
            'image': self.file_mock,
            'primary_contact': Contact.objects.all()[0].pk,
            'address': Address.objects.all()[0].pk,
            'description': 'Test description',
            'just_giving_link': 'http://www.test.com',
            'raised': -50,
            'goal': 60
        })
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 1, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['raised'], ['Raised cannot be negative'],
                         'Error not raised for negative raised field')

    def test_should_fail_if_form_deemed_valid_with_negative_goal(self):
        form = OrganisationAdminForm({
            'name': 'Test Organisation',
            'image': self.file_mock,
            'primary_contact': Contact.objects.all()[0].pk,
            'address': Address.objects.all()[0].pk,
            'description': 'Test description',
            'just_giving_link': 'http://www.test.com',
            'raised': 50,
            'goal': -60
        })
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 1, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['goal'], ['Goal cannot be negative'],
                         'Error not raised for negative goal field')


class WishlistFormTest(TestCase):

    def setUp(self):
        item_data = [['Sleeping Bag', 'Warm, durable & waterproof if possible'],
                     ['Toothbrush', 'Travel toothbrush. Non-electric.'],
                     ['Toothpaste', 'Small travel toothpaste']]

        for item in item_data:
            Item.objects.create(name=item[0], description=item[1])

        Address.objects.create(address_line="33 Test Street", county="Antrim", postcode="BT9 RGH")
        Contact.objects.create(first_name="Joe", surname="Bloggs", telephone="02890768976", mobile="07716453657",
                               email="j.bloggs@hotmail.com", description="A generic Test User",
                               address=Address.objects.get(address_line="33 Test Street"))

        Organisation.objects.create(name='Welcome Organisation', primary_contact=Contact.objects.all()[0],
                                    address=Address.objects.all()[0],
                                    description='Every year the Welcome Organisation assists around '
                                                '1,300 individuals make their journey out of homelessness.',
                                    just_giving_link='http://www.google.co.uk', raised=10, goal=50)

    def test_should_fail_if_form_deemed_invalid_with_valid_data(self):
        form = WishlistForm({
            'organisation': Organisation.objects.all()[0].pk,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(days=30),
            'reoccurring': True,
            'items': [Item.objects.get(name='Sleeping Bag').pk,
                      Item.objects.get(name='Toothbrush').pk,
                      Item.objects.get(name='Toothpaste').pk]
        })
        form.is_valid()
        self.assertTrue(form.is_valid(), 'Form was deemed invalid with valid data')

    def test_should_fail_if_form_deemed_valid_with_blank_data(self):
        form = WishlistForm({})
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 4, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['organisation'], ['This field is required.'], 'Error not raised for empty'
                                                                                   'organisation field')
        self.assertEqual(form.errors['start_time'], ['This field is required.'], 'Error not raised for empty start_time'
                                                                                 'field')
        self.assertEqual(form.errors['end_time'], ['This field is required.'],
                         'Error not raised for empty end_time field')
        self.assertEqual(form.errors['items'], ['This field is required.'], 'Error not raised for empty items field')

    def test_should_fail_if_form_deemed_valid_with_invalid_relational_data(self):
        form = WishlistForm({
            'organisation': 6,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(days=30),
            'reoccurring': True,
            'items': [Item.objects.get(name='Sleeping Bag').pk,
                      Item.objects.get(name='Toothbrush').pk,
                      8]})
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 2, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['organisation'], ['Select a valid choice. '
                                                       'That choice is not one of the available choices.'],
                         'Error not raised for non-existent organisation field')
        self.assertEqual(form.errors['items'], ['Select a valid choice. '
                                                '8 is not one of the available choices.'],
                         'Error not raised for non-existent item in items field')

    def test_should_fail_if_form_deemed_valid_with_end_time_before_start_time(self):
        form = WishlistForm({
            'organisation': Organisation.objects.all()[0].pk,
            'start_time': timezone.now() + timedelta(days=40),
            'end_time': timezone.now() + timedelta(days=30),
            'reoccurring': True,
            'items': [Item.objects.get(name='Sleeping Bag').pk,
                      Item.objects.get(name='Toothbrush').pk,
                      Item.objects.get(name='Toothpaste').pk]
        })
        form.is_valid()
        self.assertFalse(form.is_valid(), 'Form was deemed valid with invalid data')
        self.assertEqual(len(form.errors), 1, 'Different number of errors than expected raised')
        self.assertEqual(form.errors['end_time'], ['End time cannot come before start time.'])

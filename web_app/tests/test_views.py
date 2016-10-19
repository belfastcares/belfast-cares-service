from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, TestCase

from web_app.models import ContactResponse


class IndexViewTest(SimpleTestCase):

    def test_should_fail_if_valid_response_not_returned_for_index_request(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, "index.html", 'Index template not returned')


class LoginViewTest(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.admin_user = {'username': 'admin',
                           'password': 'bcadminpass123'}
        self.standard_user = {'username': 'welcomeuser1',
                              'password': 'welcomepassword'}
        self.invalid_user1 = {'username': 'invalid_user',
                              'password': 'eofjef'}
        self.invalid_user2 = {'username': 'welcomeuser1',
                              'password': 'invalid_pass'}

    def test_should_fail_if_valid_response_not_returned_for_login_request(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, 'registration/login.html', 'Login template not returned')

    def test_should_fail_if_admin_user_not_redirected_to_admin_page(self):
        response = self.client.post(reverse('login'), self.admin_user, follow=True)
        self.assertEqual(len(response.redirect_chain), 2, 'Redirect chain not a length of 1')
        self.assertEqual(response.redirect_chain[0][0], reverse('account_dashboard'), 'Initial redirect url'
                                                                                      ' not account dashboard')
        self.assertEqual(response.redirect_chain[0][1], 302, 'Initial redirect status code not 302')
        self.assertEqual(response.redirect_chain[1][0], reverse('admin:index'), 'Second redirect url not admin page')
        self.assertEqual(response.redirect_chain[1][1], 302, 'Second redirect status code not 302')
        self.assertTemplateUsed(response, 'admin/index.html', 'Admin template not used in response.')
        self.assertEqual(response.status_code, 200, 'Final status code not 200')

    def test_should_fail_if_standard_user_not_redirected_to_account_dashboard(self):
        response = self.client.post(reverse('login'), self.standard_user, follow=True)
        self.assertEqual(len(response.redirect_chain), 1, 'Redirect chain not a length of 1')
        self.assertEqual(response.redirect_chain[0][0], reverse('account_dashboard'), 'Redirect url not account'
                                                                                      'dashboard')
        self.assertEqual(response.redirect_chain[0][1], 302, 'Redirect code not 302')
        self.assertTemplateUsed(response, 'account_dashboard.html', 'Account dashboard template not used in response')
        self.assertEqual(response.status_code, 200, 'Final status code not 200')

    def test_should_fail_if_invalid_username_password_cause_redirect(self):
        response = self.client.post(reverse('login'), self.invalid_user1, follow=True)
        self.assertEqual(len(response.redirect_chain), 0, 'Redirect chain not empty')
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. '
                                                     'Note that both fields may be case-sensitive.', 'Error message'
                                                                                                     'not present'
                                                                                                     'on form')
        self.assertEqual(response.status_code, 200, 'Final status code not 200')

    def test_should_fail_if_valid_username_invalid_password_cause_redirect(self):
        response = self.client.post(reverse('login'), self.invalid_user2, follow=True)
        self.assertEqual(len(response.redirect_chain), 0, 'Redirect chain not empty')
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. '
                                                     'Note that both fields may be case-sensitive.', 'Error message not'
                                                                                                     'present on form')
        self.assertEqual(response.status_code, 200, 'Final status code not 200')


class VolunteerListingViewTest(TestCase):
    fixtures = ['initial_data']

    def test_should_fail_if_valid_response_not_returned_for_volunteer_listing_request(self):
        response = self.client.get(reverse('volunteer_listing'))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, "volunteer_listing.html", 'Volunteer listing '
                                                                       'template not returned')
        self.assertEqual(len(response.context['volunteers']), 2, 'Two volunteers in db not sent to template')


class VolunteerSingleViewTest(TestCase):
    fixtures = ['initial_data']

    def test_should_fail_if_valid_response_not_returned_for_volunteer_with_id_one(self):
        response = self.client.get(reverse('volunteer_single', kwargs={'volunteer_id': 1}))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, "volunteer_single.html", 'Volunteer single template not'
                                                                      'returned')
        self.assertEqual(response.context['volunteer'].id, 1, 'Volunteer with id 1 not sent to template')

    def test_should_fail_if_valid_response_not_returned_for_non_existent_volunteer_id(self):
        response = self.client.get(reverse('volunteer_single', kwargs={'volunteer_id': 6}))
        self.assertEqual(response.status_code, 404, 'Status code not 404')
        self.assertTemplateUsed(response, '404.html', '404 template not returned')

    def test_should_fail_if_valid_response_not_returned_for_volunteer_with_public_flag_unset(self):
        response = self.client.get(reverse('volunteer_single', kwargs={'volunteer_id': 3}))
        self.assertEqual(response.status_code, 404, 'Status code not 404')
        self.assertTemplateUsed(response, '404.html', '404 template not returned')


class OrganisationListingViewTest(TestCase):
    fixtures = ['initial_data']

    def test_should_fail_if_valid_response_not_returned_for_organisation_listing_request(self):
        response = self.client.get(reverse('organisation_listing'))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, "organisation_listing.html", 'Organisation listing '
                                                                       'template not returned')
        self.assertEqual(len(response.context['organisations']), 4, 'Four organisations in db not sent to template')


class OrganisationSingleViewTest(TestCase):
    fixtures = ['initial_data']

    def test_should_fail_if_valid_response_not_returned_for_organisation_with_id_one(self):
        response = self.client.get(reverse('organisation_single', kwargs={'organisation_id': 1}))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, "organisation_single.html", 'Organisation single template not'
                                                                      'returned')
        self.assertEqual(response.context['organisation'].id, 1, 'Organisation with id 1 not sent to template')

    def test_should_fail_if_valid_response_not_returned_for_non_existent_organisation_id(self):
        response = self.client.get(reverse('organisation_single', kwargs={'organisation_id': 6}))
        self.assertEqual(response.status_code, 404, 'Status code not 404')
        self.assertTemplateUsed(response, '404.html', '404 template not returned')


class AccountDashboard(TestCase):
    fixtures = ['initial_data']

    def test_should_fail_if_login_redirect_not_performed_for_incorrect_user_credentials_users(self):
        self.client.login(username='fred', password='secret')
        response = self.client.get(reverse('account_dashboard'), follow=True)
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(len(response.redirect_chain), 1, "Not 1 redirect in redirect chain")
        self.assertEqual(response.redirect_chain[0][0], "%s?next=%s" % (reverse('login'),
                                                                        reverse('account_dashboard')),
                         "Initial redirect url not login page")
        self.assertEqual(response.redirect_chain[0][1], 302, "Initial status code not 302")
        self.assertTemplateUsed(response, 'registration/login.html', 'Login template not used in response')

    def test_should_fail_if_login_redirect_not_performed_for_unauthenticated_users(self):
        response = self.client.get(reverse('account_dashboard'), follow=True)
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(len(response.redirect_chain), 1, "Not 1 redirect in redirect chain")
        self.assertEqual(response.redirect_chain[0][0], "%s?next=%s" % (reverse('login'),
                                                                        reverse('account_dashboard')),
                         "Initial redirect url not"
                         "login page")
        self.assertEqual(response.redirect_chain[0][1], 302, "Initial status code not 302")
        self.assertTemplateUsed(response, 'registration/login.html', 'Login template not used in response')


class HelpViewTest(SimpleTestCase):

    def test_should_fail_if_valid_response_not_returned_for_help_request(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, "help.html", 'Help template not returned')


class ContactViewTest(TestCase):

    def setUp(self):
        self.num_responses = ContactResponse.objects.count()

    def test_should_fail_if_valid_response_not_returned_for_contact_request(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertTemplateUsed(response, "contact.html", 'Contact template not returned')

    def test_should_fail_if_error_not_returned_for_empty_message_in_post(self):
        self.assertEqual(self.num_responses, 0, 'Initial number of contact responses not 0')
        response = self.client.post(reverse('contact'), {'name': 'Joe Bloggs', 'email': 'joe@hotmail.com',
                                                         'phone': '02893838943', 'message': ''})
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertFormError(response, 'form', 'message', 'This field is required.', 'Error message not present for'
                                                                                     'message field')
        self.assertEqual(ContactResponse.objects.count(), self.num_responses, 'Number of responses has changed')

    def test_should_fail_if_error_not_returned_for_invalid_email_in_post(self):
        self.assertEqual(self.num_responses, 0, 'Initial number of contact responses not 0')
        response = self.client.post(reverse('contact'), {'name': 'Joe Bloggs', 'email': 'joehotmail.com',
                                                         'phone': '02893838943', 'message': 'Test message'})
        self.assertEqual(response.status_code, 200, 'Status code not 200')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.', 'Error message not present for'
                                                                                        'email field')
        self.assertEqual(ContactResponse.objects.count(), self.num_responses, 'Number of responses has changed')

    def test_should_fail_if_contact_responses_not_increased_for_valid_post(self):
        response = self.client.post(reverse('contact'), {'name': 'Joe Bloggs', 'email': 'joe@hotmail.com',
                                                         'phone': '02893838943', 'message': 'Test message'},
                                    follow=True)
        self.assertEqual(ContactResponse.objects.count(), self.num_responses + 1,
                         'Number of contact responses in db not'
                         'increased by 1')
        self.assertEqual(len(response.redirect_chain), 1, "Not 1 redirect in redirect chain")
        self.assertEqual(response.redirect_chain[0][0], reverse('contact'), 'Initial redirect url not contact page')
        self.assertEqual(response.redirect_chain[0][1], 302, 'Initial status code not 302')
        self.assertEqual(response.status_code, 200, 'Final status code not 200')

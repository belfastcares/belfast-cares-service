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


class RegisterOrganisationTest(TestCase):
    def setUp(self):
        self.valid_form_data = (
            {'organisation_info-name': 'Test',
             'organisation_info-description': 'Test description',
             'organisation_info-just_giving_link': 'http://www.google.co.uk',
             'organisation_info-raised': 10,
             'organisation_info-goal': 100,
             'organisation_info-address_line': 'testing',
             'organisation_info-county': 'test',
             'organisation_info-postcode': 'BT19 TST',
             'register_organisation_wizard-current_step': 'organisation_info',
             },
            {
                'primary_contact_info-first_name': 'Joe',
                'primary_contact_info-surname': 'Bloggs',
                'primary_contact_info-telephone': '02890876576',
                'primary_contact_info-mobile': '07786459078',
                'primary_contact_info-email': 'jbloggs@test.com',
                'primary_contact_info-description': 'Test description',
                'primary_contact_info-address_line': '123 Test Street',
                'primary_contact_info-county': 'Test County',
                'primary_contact_info-postcode': 'BT9 TSR',
                'register_organisation_wizard-current_step': 'primary_contact_info',
            },
            {
                'organisation_accounts-username': 'test123',
                'organisation_accounts-password1': 'password123',
                'organisation_accounts-password2': 'password123',
                'organisation_accounts-first_name': 'Joe',
                'organisation_accounts-surname': 'Bloggs',
                'organisation_accounts-telephone': '02890876576',
                'organisation_accounts-mobile': '07786459078',
                'organisation_accounts-email': 'jbloggs@test.com',
                'organisation_accounts-description': 'Test description',
                'organisation_accounts-address_line': 'testing',
                'organisation_accounts-county': 'test',
                'organisation_accounts-postcode': 'BT10 test',
                'register_organisation_wizard-current_step': 'organisation_accounts',
            },
            {
                'wishlist_info-start_time': '2006-10-25 14:30:59',
                'wishlist_info-end_time': '2006-10-26 14:30:59',
                'wishlist_info-reoccuring': 'on',
                'wishlist_info-items': ['1', '2'],
                'wishlist_info-INITIAL_FORMS': '0',
                'wishlist_info-TOTAL_FORMS': '3',
                'wishlist_info-MAX_NUM_FORMS': '3',
                'wishlist_info-MIN_NUM_FORMS': '3',
                'wishlist_info-0-id': '',
                'wishlist_info-0-name': 'Test Item',
                'wishlist_info-0-description': 'The first test item',
                'wishlist_info-1-id': '',
                'wishlist_info-1-name': 'Test Item 2',
                'wishlist_info-1-description': 'The second test item',
                'wishlist_info-2-id': '',
                'wishlist_info-2-name': '',
                'wishlist_info-2-description': '',
                'register_organisation_wizard-current_step': 'wishlist_info',
            }
        )

    def test_should_fail_if_valid_response_not_returned_for_register_request(self):
        response = self.client.get(reverse('register_organisation_wizard'), follow=True)
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        # We expect the wizard to redirect to the step 1 URL
        self.assertEqual(len(response.redirect_chain), 1, "Not 1 redirect in redirect chain")
        self.assertEqual(response.redirect_chain[0][0], reverse('register_organisation_wizard_step',
                                                                kwargs={'step': 'organisation_info'}),
                         "Redirect URL not step 1")
        self.assertEqual(response.redirect_chain[0][1], 302, "Initial status code not 302")
        self.assertTemplateUsed(response, "registration/organisation/register_organisation_step_1.html",
                                'wizard step 1 template not used in response')
        wizard = response.context['wizard']
        self.assertEqual(wizard['steps'].current, 'organisation_info', 'Invalid current step')
        self.assertEqual(wizard['steps'].step0, 0, 'Invalid step 0')
        self.assertEqual(wizard['steps'].step1, 1, 'Invalid step 1')
        self.assertEqual(wizard['steps'].last, 'wishlist_info', 'Invalid last step')
        self.assertEqual(wizard['steps'].prev, None, 'Invalid previous step')
        self.assertEqual(wizard['steps'].next, 'primary_contact_info', 'Invalid next step')
        self.assertEqual(wizard['steps'].count, 4, 'Invalid total steps')
        self.assertEqual(wizard['url_name'], 'register_organisation_wizard_step', 'Invalid current URL')

    def test_should_fail_if_errors_not_returned_for_blank_step1_data(self):
        response = self.client.post(reverse('register_organisation_wizard_step', kwargs={'step': 'organisation_info'}),
                                    {'register_organisation_wizard-current_step': 'organisation_info'})
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'organisation_info', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 2, 'Invalid number of errors for org info'
                                                                                'form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'name': ['This field is required.'],
                          'description': ['This field is required.']}, 'Invalid errors returned for org info form')
        self.assertEqual(len(response.context['wizard']['forms'][1].errors), 3,
                         'Invalid number of errors for org address'
                         'form')
        self.assertEqual(response.context['wizard']['forms'][1].errors,
                         {'address_line': ['This field is required.'],
                          'county': ['This field is required.'],
                          'postcode': ['This field is required.']}, 'Invalid errors returned for org address form')

    def test_should_fail_if_errors_not_returned_for_invalid_step1_data(self):
        data = self.valid_form_data[0]
        data['organisation_info-just_giving_link'] = 'invalid'
        data['organisation_info-raised'] = -10,
        data['organisation_info-goal'] = -10

        response = self.client.post(reverse('register_organisation_wizard_step', kwargs={'step': 'organisation_info'}),
                                    data)
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'organisation_info', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 3,
                         'Invalid number of errors for org info form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'goal': ['Goal cannot be negative'],
                          'raised': ['Raised cannot be negative'],
                          'just_giving_link': ['Enter a valid URL.']}, 'Invalid errors returned for org info form')

    def test_should_fail_if_errors_returned_for_valid_step1_data(self):
        response = self.client.post(reverse('register_organisation_wizard_step', kwargs={'step': 'organisation_info'}),
                                    self.valid_form_data[0], follow=True)
        self.assertEqual(response.redirect_chain[0][0], reverse('register_organisation_wizard_step',
                                                                kwargs={'step': 'primary_contact_info'}),
                         'Initial redirect url not step 2')
        self.assertEqual(response.redirect_chain[0][1], 302, 'Initial status code not 302')
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        wizard = response.context['wizard']
        self.assertEqual(wizard['steps'].current, 'primary_contact_info', 'Invalid current step')
        self.assertEqual(wizard['steps'].step0, 1, 'Invalid step0')
        self.assertEqual(wizard['steps'].prev, 'organisation_info', 'Invalid previous step')
        self.assertEqual(wizard['steps'].next, 'organisation_accounts', 'Invalid next step')

    def test_should_fail_if_errors_not_returned_for_blank_step2_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'primary_contact_info'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'primary_contact_info'}),
                                    {'register_organisation_wizard-current_step': 'primary_contact_info'})
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'primary_contact_info', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 3,
                         'Invalid number of errors for primary contact'
                         ' info form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'first_name': ['This field is required.'],
                          'surname': ['This field is required.'],
                          'email': ['This field is required.']},
                         'Invalid errors returned for primary contact info form')
        self.assertEqual(len(response.context['wizard']['forms'][1].errors), 3,
                         'Invalid number of errors for primary contact'
                         ' address form')
        self.assertEqual(response.context['wizard']['forms'][1].errors,
                         {'address_line': ['This field is required.'],
                          'county': ['This field is required.'],
                          'postcode': ['This field is required.']}, 'Invalid errors returned for primary contact '
                                                                    'address form')

    def test_should_fail_if_errors_not_returned_for_invalid_step2_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'primary_contact_info'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        data = self.valid_form_data[1]
        data['primary_contact_info-email'] = 'invalid email'

        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'primary_contact_info'}), data)
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'primary_contact_info', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 1,
                         'Invalid number of errors for primary contact'
                         ' info form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'email': ['Enter a valid email address.']},
                         'Invalid errors returned for primary contact info form')

    def test_should_fail_if_errors_returned_for_valid_step2_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'primary_contact_info'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'primary_contact_info'}),
                                    self.valid_form_data[1], follow=True)
        self.assertEqual(response.redirect_chain[0][0], reverse('register_organisation_wizard_step',
                                                                kwargs={'step': 'organisation_accounts'}),
                         'Initial redirect url not step 3')
        self.assertEqual(response.redirect_chain[0][1], 302, 'Initial status code not 302')
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        wizard = response.context['wizard']
        self.assertEqual(wizard['steps'].current, 'organisation_accounts', 'Invalid current step')
        self.assertEqual(wizard['steps'].step0, 2, 'Invalid step0')
        self.assertEqual(wizard['steps'].prev, 'primary_contact_info', 'Invalid previous step')
        self.assertEqual(wizard['steps'].next, 'wishlist_info', 'Invalid next step')

    def test_should_fail_if_errors_not_returned_for_blank_step3_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'organisation_accounts'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'organisation_accounts'}),
                                    {'register_organisation_wizard-current_step': 'organisation_accounts'})
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'organisation_accounts', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 3,
                         'Invalid number of errors for org user login form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'username': ['This field is required.'],
                          'password1': ['This field is required.'],
                          'password2': ['This field is required.']},
                         'Invalid errors returned for org user login form')
        self.assertEqual(len(response.context['wizard']['forms'][1].errors), 3,
                         'Invalid number of errors for org user'
                         ' contact form')
        self.assertEqual(response.context['wizard']['forms'][1].errors,
                         {'first_name': ['This field is required.'],
                          'surname': ['This field is required.'],
                          'email': ['This field is required.']},
                         'Invalid errors returned for org user contact form')
        self.assertEqual(len(response.context['wizard']['forms'][2].errors), 3,
                         'Invalid number of errors for org user'
                         ' address form')
        self.assertEqual(response.context['wizard']['forms'][2].errors,
                         {'address_line': ['This field is required.'],
                          'county': ['This field is required.'],
                          'postcode': ['This field is required.']}, 'Invalid errors returned for org user '
                                                                    'address form')

    def test_should_fail_if_errors_not_returned_for_invalid_step3_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'organisation_accounts'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        data = self.valid_form_data[2]
        data['organisation_accounts-username'] = ')!(*"!*"&!(*"^!'
        data['organisation_accounts-password1'] = 'password'
        data['organisation_accounts-password2'] = 'password'
        data['organisation_accounts-email'] = 'invalid email'

        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'organisation_accounts'}), data)
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'organisation_accounts', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 2,
                         'Invalid number of errors for org user'
                         ' login form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'username': ['Enter a valid username. This value may contain only letters,'
                                       ' numbers and @/./+/-/_ characters.'],
                          'password2': ['This password is too common.']},
                         'Invalid errors returned for org user login form')
        self.assertEqual(len(response.context['wizard']['forms'][1].errors), 1,
                         'Invalid number of errors for org user'
                         ' contact form')
        self.assertEqual(response.context['wizard']['forms'][1].errors,
                         {'email': ['Enter a valid email address.']},
                         'Invalid errors returned for org user contact form')

    def test_should_fail_if_errors_not_returned_for_non_matching_step3_password_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'organisation_accounts'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        data = self.valid_form_data[2]
        data['organisation_accounts-password1'] = 'password'
        data['organisation_accounts-password2'] = 'password2'

        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'organisation_accounts'}), data)
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'organisation_accounts', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 1,
                         'Invalid number of errors for org user'
                         ' login form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'password2': ["The two password fields didn't match."]},
                         'Invalid errors returned for org user login form')

    def test_should_fail_if_errors_returned_for_valid_step3_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'organisation_accounts'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'organisation_accounts'}),
                                    self.valid_form_data[2], follow=True)
        self.assertEqual(response.redirect_chain[0][0], reverse('register_organisation_wizard_step',
                                                                kwargs={'step': 'wishlist_info'}),
                         'Initial redirect url not step 4')
        self.assertEqual(response.redirect_chain[0][1], 302, 'Initial status code not 302')
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        wizard = response.context['wizard']
        self.assertEqual(wizard['steps'].current, 'wishlist_info', 'Invalid current step')
        self.assertEqual(wizard['steps'].step0, 3, 'Invalid step0')
        self.assertEqual(wizard['steps'].prev, 'organisation_accounts', 'Invalid previous step')
        self.assertEqual(wizard['steps'].next, None, 'Invalid next step')

    def test_should_fail_if_errors_not_returned_for_blank_step4_data(self):
        response = self.client.get(reverse('register_organisation_wizard_step',
                                           kwargs={'step': 'wishlist_info'}))
        self.assertEqual(response.status_code, 200, "Initial status code not 200")
        response = self.client.post(reverse('register_organisation_wizard_step',
                                            kwargs={'step': 'wishlist_info'}),
                                    {'register_organisation_wizard-current_step': 'wishlist_info',
                                     'wishlist_info-INITIAL_FORMS': '0',
                                     'wishlist_info-MAX_NUM_FORMS': '3',
                                     'wishlist_info-MIN_NUM_FORMS': '0',
                                     'wishlist_info-TOTAL_FORMS': '3',
                                     })
        self.assertEqual(response.status_code, 200, "Final status code not 200")
        self.assertEqual(response.context['wizard']['steps'].current, 'wishlist_info', 'Invalid current step')
        self.assertEqual(len(response.context['wizard']['forms'][0].errors), 3,
                         'Invalid number of errors for wishlist info form')
        self.assertEqual(response.context['wizard']['forms'][0].errors,
                         {'start_time': ['This field is required.'],
                          'end_time': ['This field is required.'],
                          'items': ['This field is required.']},
                         'Invalid errors returned for wishlist info form')

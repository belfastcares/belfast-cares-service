import os

import datetime
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base_site.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

from web_app.models import *

def setup_items():
    item_data = [['Sleeping Bag', 'Warm, durable & waterproof if possible'],
    ['Toothbrush', 'Travel toothbrush. Non-electric.'],
    ['Toothpaste', 'Small travel toothpaste'],
    ['Mens Winter Socks', 'New mens winter socks.'],
    ['Womens Winter Socks', '''New womens' winter socks.'''],
    ['Cutlery', 'All cutlery welcome. Should be clean and considered usable by others.']]

    for item in item_data:
        temp_item = Item(name=item[0], description=item[1])
        temp_item.save()

def setup_addresses():
    address_data = [['Unit 36, Townsend Enterprise Park, Townsend St, Belfast', 'Antrim', 'BT13 2ES'],
    ['187 Stranmillis Road, Belfast', 'Antrim', 'BT9 5EE'],
    ['4th Floor, Andras House, 60 Great Victoria St, Belfast', 'Antrim', 'BT2 7BB'],
    ['25-27 Franklin St, Belfast', 'Antrim', 'BT2 8DS'],
    ['196-200 Antrim Road, Belfast', 'Antrim', 'BT15 2AJ']]

    for address in address_data:
        temp_address = Address(address_line =address[0], county=address[1], postcode=address[2])
        temp_address.save()

def setup_contacts():
    contact_data = [['Outreach', 'Team', '02890 000 000', '07894 931 047', 'welcome@organisation.com', 'The outreach team is a component of the Welcome Organisation'],
                    ['Aileen', 'Coney', '028 9035 1561', '028 9000 0000', 'info@svpni.co.uk', 'Director of St. Vincent de Paul'],
                    ['Council for the Homeless', 'NI', '028 9024 6440', '028 9000 0000', 'contact@chni.com', 'Leader of Council for the Homeless NI'],
                    ['Central', 'Office', '028 90 232 882', '028 9000 0000', 'info@simoncommunity.org', 'The main office for the Simon Community']]

    for count, contact in enumerate(contact_data,1):
        temp_contact = Contact(first_name=contact[0], surname=contact[1], telephone=contact[2], mobile=contact[3],
                               email=contact[4], description=contact[5], address=Address.objects.get(pk=count))
        temp_contact.save()

def setup_organisations():
    welcome_organisation = Organisation(name='Welcome Organisation', primary_contact = Contact.objects.get(pk=1), address = Address.objects.get(pk=1),
                          description= 'Every year the Welcome Organisation assists around 1,300 individuals make their journey out of homelessness.',
                                       just_giving_link= 'http://www.google.co.uk', raised=10, goal=50)
    welcome_organisation.save()

    st_vincent_de_paul = Organisation(name='St. Vincent de Paul', primary_contact = Contact.objects.get(pk=2), address = Address.objects.get(pk=5),
                          description= 'No work of charity is foreign to the society. Our work through person to '
                                       'person contact encompasses every form of aid that alleviates suffering and '
                                       'promotes the dignity of mankind. The society strives not only to alleviate need'
                                       ' but also to discover and redress the situations which cause it. It services '
                                       'everyone in need, regardless of creed, opinion,colour, origin or caste.',
                                       just_giving_link= 'http://www.twitter.com', raised=60, goal=500)
    st_vincent_de_paul.save()

    council_for_the_homeless = Organisation(name='Council for the Homeless NI', primary_contact = Contact.objects.get(pk=3), address = Address.objects.get(pk=3),
                          description= 'Founded in 1983, we are the sole representative organisation for those working '
                                       'with and supporting homeless people across Northern Ireland. We are the '
                                       'independent voice of the sector.',
                                       just_giving_link= 'http://www.reddit.com', raised=5, goal=1000)
    council_for_the_homeless.save()

    simon_community = Organisation(name='Simon Community', primary_contact = Contact.objects.get(pk=4), address = Address.objects.get(pk=4),
                          description= "Established in 1971 in response to a homelessness crisis in Belfast, "
                                       "Simon Community has grown to become Northern Ireland's leading homelessness charity "
                                       "and service provider. From a beginning of just one house, two full time staff and a "
                                       "few volunteers in Belfast, Simon Community NI now helps over 3000 people every year "
                                       "across 22 projects throughout Northern Ireland with a staff count of 300 and 50 "
                                       "volunteers. We work without judgement to support people who are, or are at risk of, "
                                       "becoming homeless.",
                                       just_giving_link= 'http://www.youtube.com', raised=5100, goal=5000)
    simon_community.save()


def setup_wishlists():
    welcome_wish = Wishlist(organisation=Organisation.objects.get(pk=1), start_time=timezone.now(),
                            end_time=timezone.now()+datetime.timedelta(days=30), reoccurring=False)
    welcome_wish.save()
    welcome_wish.items.add(1,2,3)

    st_vincent_de_paul_wish = Wishlist(organisation=Organisation.objects.get(pk=2), start_time=timezone.now(),
                                  end_time=timezone.now()+datetime.timedelta(days=60), reoccurring=False)
    st_vincent_de_paul_wish.save()
    st_vincent_de_paul_wish.items.add(1,2,5,6)

    council_for_the_homeless_wish = Wishlist(organisation=Organisation.objects.get(pk=3), start_time=timezone.now(),
                                  end_time=timezone.now()+datetime.timedelta(days=20), reoccurring=True)
    council_for_the_homeless_wish.save()
    council_for_the_homeless_wish.items.add(1,4,2)

    simon_community_wish = Wishlist(organisation=Organisation.objects.get(pk=4), start_time=timezone.now(),
                                  end_time=timezone.now()+datetime.timedelta(days=150), reoccurring=True)
    simon_community_wish.save()
    simon_community_wish.items.add(1,3,4,5,6)


def setup_organisation_user():
    welcome_org_user = OrganisationUser(user=User.objects.create_user(username='welcomeuser1',
                                    password='welcomepassword'), contact=Contact.objects.get(pk=1),
                                        organisation=Organisation.objects.get(pk=1))
    welcome_org_user.save()

    st_vincent_de_paul_org_user = OrganisationUser(user=User.objects.create_user(username='stvincentuser1',
                                    password='vincentpassword'), contact=Contact.objects.get(pk=2),
                                        organisation=Organisation.objects.get(pk=2))
    st_vincent_de_paul_org_user.save()

    council_for_the_homeless_org_user = OrganisationUser(user=User.objects.create_user(username='counciluser1',
                                    password='councilpassword'), contact=Contact.objects.get(pk=3),
                                        organisation=Organisation.objects.get(pk=3))
    council_for_the_homeless_org_user.save()

    simon_community_org_user = OrganisationUser(user=User.objects.create_user(username='simonuser1',
                                    password='simonpassword'), contact=Contact.objects.get(pk=4),
                                        organisation=Organisation.objects.get(pk=4))
    simon_community_org_user.save()



if __name__ == "__main__":
    setup_addresses()
    setup_contacts()
    setup_organisations()
    setup_items()
    setup_wishlists()
    setup_organisation_user()

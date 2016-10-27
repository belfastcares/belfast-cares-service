import web_app.views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework.authtoken import views
from web_app.viewsets import *

admin.autodiscover()

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'address', AddressViewSet)
router.register(r'items', ItemViewSet)
router.register(r'organisation', OrganisationViewSet)
router.register(r'wishlist', WishlistViewSet)
router.register(r'organisationuser', OrganisationUserViewSet)
router.register(r'contactresponse', ContactResponseViewSet)
router.register(r'volunteers', VolunteerViewSet)

urlpatterns = [
    url(r'^$', web_app.views.index, name='index'),

    url(r'^contact/$', web_app.views.contact, name='contact'),
    url(r'^help/$', web_app.views.help, name='help'),

    url(r'^volunteers/$', web_app.views.volunteer_listing, name='volunteer_listing'),
    url(r'^volunteer/(?P<volunteer_id>\w{1,50})/$', web_app.views.volunteer_single, name='volunteer_single'),

    url(r'^organisations/$', web_app.views.organisation_listing, name='organisation_listing'),
    url(r'^organisation/(?P<organisation_id>\w{1,50})/$', web_app.views.organisation_single,
        name='organisation_single'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^register/organisation/$', web_app.views.registration_organisation_wizard_view, name='register_organisation'),
    url(r'^register/volunteer/$', web_app.views.register_volunteer, name='register_volunteer'),

    url(r'^account/dashboard/$', web_app.views.account_dashboard, name='account_dashboard'),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^manage/', include(admin.site.urls)),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
]

# We are only want to serve the media directory here for testing purposes
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

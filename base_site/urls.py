import web_app.views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    url(r'^$', web_app.views.index, name='index'),
    url(r'^contact/$', web_app.views.contact, name='contact'),
    url(r'^help/$', web_app.views.help, name='help'),
    url(r'^volunteer/(?P<volunteer_id>\w{1,50})/$', web_app.views.volunteer_single, name='volunteer_single'),
    url(r'^organisations/$', web_app.views.organisation_listing, name='organisation_listing'),
    url(r'^organisation/(?P<organisation_id>\w{1,50})/$', web_app.views.organisation_single, name='organisation_single'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^account/dashboard/$', web_app.views.account_dashboard, name='account_dashboard'),
    url(r'^admin/', include(admin.site.urls))
]

# We are only want to serve the media directory here for testing purposes
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
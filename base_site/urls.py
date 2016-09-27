import web_app.views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^$', web_app.views.index, name='index'),
    url(r'^login', web_app.views.login, name='login'),
    url(r'^contact', web_app.views.contact, name='contact'),
    url(r'^help', web_app.views.help, name='help'),
    url(r'^volunteer/(?P<volunteer_id>\w{1,50})/$', web_app.views.volunteer_single, name='volunteer_single'),
    url(r'^charities', web_app.views.charities_listing, name='charities_listing'),
    url(r'^charity/(?P<charity_id>\w{1,50})/$', web_app.views.charities_single, name='charities_single'),
    url(r'^admin/', include(admin.site.urls))
]

# We are only want to serve the media directory here for testing purposes
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
import web_app.views
from django.conf.urls import include, url
from django.contrib import admin

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

import web_app.views
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', web_app.views.index, name='index'),
    url(r'^login', web_app.views.login, name='login'),
    url(r'^contact', web_app.views.contact, name='contact'),
    url(r'^volunteers', web_app.views.volunteer_listing, name='volunteer_listing'),
    url(r'^volunteer', web_app.views.volunteer_listing, name='volunteer_single'),
    url(r'^charities', web_app.views.volunteer_listing, name='charities_listing'),
    url(r'^charity', web_app.views.volunteer_listing, name='charities_single'),
    url(r'^admin/', include(admin.site.urls)),
]

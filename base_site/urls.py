from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import web_app.views

urlpatterns = [
    url(r'^$', web_app.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]

from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import web_app.views

# Examples:
# url(r'^$', 'base_site.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', web_app.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]

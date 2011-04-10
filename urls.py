from django.conf.urls.defaults import *


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    # (r'^guide_to_testing/', include('guide_to_testing.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^polls/', include('polls.urls')),
)

from django.conf.urls.defaults import *


urlpatterns = patterns('polls.views',
    url(r'^$', 'index', name='polls_index'),
    url(r'^(?P<poll_id>\d+)/$', 'detail', name='polls_detail'),
    url(r'^(?P<poll_id>\d+)/results/$', 'results', name='polls_results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'vote', name='polls_vote'),
)

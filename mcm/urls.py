from django.conf.urls.defaults import *

urlpatterns = patterns('cost_management.mcm.views',
    (r'^$', 'index'),
    (r'^item/$', 'item'),
    (r'^monthly/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'monthly'),
    (r'^user/(?P<user_name>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'user_transaction'),
    (r'^avg_diff/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'avg_diff')
)

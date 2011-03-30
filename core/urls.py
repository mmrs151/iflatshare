from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    (r'^$', 'index'),
    (r'^item/$', 'item'),
    (r'^monthly/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'monthly'),
    (r'^user/(?P<user_name>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'user_transaction'),     
    (r'^avg_diff/', 'avg_diff'),
    (r'^category/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'monthly_category'),
    (r'^category/(?P<category_name>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'category_transaction'),
    (r'^profile/address/edit/$', 'edit_address'),
    (r'^thanks/$', 'thanks'),
    (r'^flatmate/create/$', 'create_flatmate'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('cost_management.mcm.views',
    (r'^$', 'index'),
    (r'^item/$', 'item'),
    (r'^list/$', 'item_list')
)

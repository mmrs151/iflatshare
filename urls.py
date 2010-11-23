from django.conf.urls.defaults import *
from django.conf import settings
from core.forms import IFLContactForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
                                                                        'show_indexes': True}),
    )

urlpatterns += patterns('',
    (r'', include('iflatshare.core.urls')),
 )
 
contact_info = {'form_class':IFLContactForm, 
                'template_name':'envelope/contact.html', 'redirect_to':'/thanks/',}

urlpatterns += patterns('',
    url(r'^contact/', 'envelope.views.contact', kwargs=contact_info, name='envelope-contact'),
)                

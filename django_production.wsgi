import os
import sys
import site

site.addsitedir('/sites/iflatshare_prod/lib/python2.6/site-packages')
sys.path.append('/sites/iflatshare_prod/current')
sys.path.append('/sites/iflatshare_prod/current/iflatshare')

os.environ['DJANGO_SETTINGS_MODULE'] = 'iflatshare.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import os
import sys

sys.path.append('/Users/shohag/Sites')
sys.path.append('/Users/shohag/Sites/iflatshare')

os.environ['DJANGO_SETTINGS_MODULE'] = 'iflatshare.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

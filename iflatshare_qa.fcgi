#!/home2/sewinzco/.local/bin/python
import sys, os
# Add a custom Python path.
sys.path.append('/home2/sewinzco/.local/lib/python2.6')
sys.path.append('/home2/sewinzco/.local/lib/python2.6/site-packages')
sys.path.append('/home2/sewinzco/.local/lib/python2.6/site-packages/flup-1.0.2-py2.6.egg')
sys.path.append('/home2/sewinzco/.local/lib/python2.6/site-packages/django')
sys.path.append('/home2/sewinzco/www')
# Switch to the directory of your project. (Optional.)
os.environ['DJANGO_SETTINGS_MODULE'] = "iflatshare.qa.iflatshare.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")


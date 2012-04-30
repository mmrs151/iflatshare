from piston.resource import Resource
from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from api.handlers import *

auth = HttpBasicAuthentication(realm="Basic Authentication")

address_handler = Resource(AddressHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^address\.(?P<emitter_format>.+)', address_handler),
)

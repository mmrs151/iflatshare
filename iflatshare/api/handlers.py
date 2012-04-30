from piston.handler import BaseHandler
from core.models import *

class AddressHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Address

    def read(self, request):  
        return {'user': request.user.is_authenticated(),
                'address': request.user.profile.address }

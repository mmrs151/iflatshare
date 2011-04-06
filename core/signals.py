from django.contrib.auth.models import User
from core.models import Profile

def create_profile(sender, **kw):
    u = kw['request'].POST['username']
    user = User.objects.get(username=u)
    if kw["signal"]:
        profile = Profile(user=user)
        profile.save()

from registration.signals import user_registered
user_registered.connect(create_profile)

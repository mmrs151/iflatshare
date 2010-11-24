def create_profile(sender, instance, **kwargs):
    print sender, instance

def assign_address(sender, instance, **kwargs):
    invitee_profile = instance
    if invitee_profile.was_invited() and invitee_profile.address is None:
        invitee_profile.address = invitee_profile.from_user_address()
        invitee_profile.save()

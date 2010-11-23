from django.forms import ModelForm
from django import forms
from models import Item, Address
from envelope.forms import *

class ItemForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = user.profile.get_housemates()

    name = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Item

class AddressForm(ModelForm):
    class Meta:
        model = Address

class CalendarForm(forms.Form):
    year = forms.DecimalField(max_digits=4)
    month = forms.DecimalField(max_digits=2, max_value=12)

class IFLContactForm(ContactForm):
    category = forms.CharField(required=False, widget=forms.HiddenInput())

    def send(self):
        u"""
        Sends the message.
        """
        subject_intro = getattr(settings, 'ENVELOPE_SUBJECT_INTRO',
                                u"")
        subject = subject_intro + self.cleaned_data['subject']
        dictionary = self.cleaned_data.copy()
        message = render_to_string('envelope/email_body.txt', dictionary)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.DEFAULT_TO_EMAIL]
        try:
            send_mail(subject, message, from_email, to_email)
            logger.info(u"Contact form submitted and sent (from: %s)" % self.cleaned_data['email'])
        except SMTPException, e:
            logger.error(u"Contact form error (%s)" % e)
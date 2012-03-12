from django.forms import ModelForm, widgets
from django import forms
from django.contrib.auth.models import User 
from models import *
from envelope.forms import *
from django.conf import settings


class ItemForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = user.profile.get_user()
        self.fields['user'].empty_label = None
        self.fields['user'].initial = user
        self.fields['category'] = forms.ModelChoiceField(queryset=user.profile.address.categories.all())
    name = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Item

class AddressForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), widget=forms.SelectMultiple(attrs={'size':'4'}))
    
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

class FlatmateCreateForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(initial=settings.DEFAULT_PASSWORD, \
                               widget=forms.HiddenInput())

    def clean_name(self):
        cleaned_data = self.cleaned_data
        clean_name = cleaned_data['name']
        clean_name = clean_name.strip()
        clean_name = clean_name.split()
        if len(clean_name) > 1:
            raise forms.ValidationError(u'User name can not have space.')
        if User.objects.filter(username=clean_name):
            raise forms.ValidationError(u'Username already taken.')
        return clean_name

from django.forms import ModelForm
from django import forms
from models import Item, Address

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


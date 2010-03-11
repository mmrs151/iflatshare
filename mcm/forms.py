from django.forms import ModelForm
from django import forms
from models import Item, User

class ItemForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = user.get_housemates()

    name = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Item

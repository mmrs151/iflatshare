from django.forms import ModelForm
from django import forms
from models import Item

class ItemForm(ModelForm):
    name = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Item
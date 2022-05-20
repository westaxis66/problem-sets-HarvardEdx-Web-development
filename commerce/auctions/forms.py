from django.forms import ModelForm
from django import forms

from .models import Listing, Bid, Comment

class PostListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'80'}))
    begining_bid = forms.CharField(widget=forms.NumberInput(attrs={'step':'0.01', 'min':'0'}))
    image = forms.CharField(widget=forms.URLInput())
    category = forms.CharField(widget=forms.Textarea(attrs={'rows':'1', 'cols':'20'}))
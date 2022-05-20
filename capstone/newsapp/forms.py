from django import forms


class subscriptionForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea(attrs={'rows':'1', 'cols':'50'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'size': 50}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': 50}))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'size': 50}))
    

class loginForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea(attrs={'rows':'1', 'cols':'50'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': 50}))
   
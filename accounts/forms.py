from django import forms
from core.models import customUser


class userForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=14, required=True)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=4, widget=forms.PasswordInput())

    class Meta():
        model = customUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password')
        help_texts = {
            'username': None,
        }
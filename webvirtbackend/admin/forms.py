from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AdminAuthForm(AuthenticationForm):
    username = forms.CharField(
        label=("Email"),
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

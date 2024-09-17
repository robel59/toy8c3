# forms.py

from django import forms
from .models import Client, Recipt

class LoginForm(forms.Form):
    guest_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ['guest_name', 'guest_email', 'guest_phone', 'password']
        widgets = {'password': forms.PasswordInput}


class ReceiptUploadForm(forms.ModelForm):
    images = forms.ImageField()

    class Meta:
        model = Recipt
        fields = ['images']

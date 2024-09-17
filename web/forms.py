# myapp/forms.py
from django import forms
from django.db import models
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from django.contrib.auth.forms import AuthenticationForm

class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'


def generate_unique_username():
    while True:
        # Generate a random suffix of length 6
        username = get_random_string(length=6)
        # Check if the generated username already exists
        if not User.objects.filter(username=username).exists():
            return username




class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)  # Make sure you have the email field here

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = generate_unique_username()#user.email  # Set username to email value
        if commit:
            user.save()
        return user


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))


class OrderFormModel(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderFormModel #{self.pk} - {self.service.title}"
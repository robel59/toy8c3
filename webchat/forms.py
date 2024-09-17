# chat/forms.py

from django import forms
from .models import ChatUser

class ChatUserForm(forms.ModelForm):
    class Meta:
        model = ChatUser
        fields = ['name', 'email', 'phone_number']

from django import forms
from django.contrib.auth.models import User
from base.models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['host', 'participants']

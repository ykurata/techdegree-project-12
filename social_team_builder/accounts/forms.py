from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model =User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email address"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('image', 'bio', 'skill')

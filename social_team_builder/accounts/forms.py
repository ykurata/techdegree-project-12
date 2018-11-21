from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from . import models


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email address"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('image', 'bio')


class SkillForm(forms.ModelForm):
    class Meta:
        model = models.Skill
        fields = ('name',)


SkillFormSet = forms.modelformset_factory(
    models.Skill,
    form=SkillForm,
    extra=1,
)

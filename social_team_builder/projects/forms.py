from django import forms

from . import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = ()

ProjectFormSet = forms.inlineformset_factory(
    models.Project,
    models.Position,
    form=ProjectForm,
    fields=("title", "description", "skill"),
    extra=1
)

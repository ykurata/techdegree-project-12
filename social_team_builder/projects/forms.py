from django import forms
from . import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            "title",
            "description",
             "estimated_time",
             "requirements"
        ]



class PositionForm(forms.ModelForm):
    class Meta:
        model = models.Position
        fields = [
            "title",
            "description",
            "skill",
            "position_filled"
        ]


PositionFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionForm,
    extra=1,
)

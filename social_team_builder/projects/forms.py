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

PositionInlineFormSet = forms.inlineformset_factory(
    models.Project,
    models.Position,
    formset=PositionFormSet,
    fields=("title", "description", "skill", "position_filled"),
    can_delete=False,
)

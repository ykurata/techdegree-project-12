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
)


PositionInlineFormSet = forms.inlineformset_factory(
    models.Project,
    models.Position,
    extra=1,
    fields=('title', 'description', 'skill', 'position_filled', ),
    formset=PositionFormSet,
    min_num=1,
    can_delete=True,
)

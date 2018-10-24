from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from . import models
from . import forms

class ProjectList(generic.ListView):
    context_object_name = "projects"
    model = models.Project


class ProjectPositionCreate(generic.CreateView):
    fields = ("title", "description", "estimated_time", "requirements")
    model = models.Project

    def get_context_data(self, **kwargs):
        data = super(ProjectPositionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['project'] = forms.ProjectFormSet(self.request.POST)
        else:
            data['project'] = forms.ProjectFormSet()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProjectPositionCreate, self).form_valid(form)


class ProjectDetail(generic.DetailView):
    model = models.Project


class ProjectUpdate(generic.UpdateView):
    fields = ("title", "description", "estimated_time", "requirements")
    model = models.Project


class PositionList(generic.ListView):
    context_object_name = "positions"
    model = models.Position


class PositionCreate(generic.CreateView):
    fields = ("title", "description", "skill")
    model = models.Position

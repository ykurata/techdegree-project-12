from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from . import models


class ProjectList(generic.ListView):
    context_object_name = "projects"
    model = models.Project


class ProjectCreate(generic.CreateView):
    fields = ("title", "description", "timeline", "requirements")
    model = models.Project

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProjectCreate, self).form_valid(form)


class ProjectDetail(generic.DetailView):
    model = models.Project


class ProjectUpdate(generic.UpdateView):
    fields = ("title", "description", "timeline", "requirements")
    model = models.Project


class PositionList(generic.ListView):
    context_object_name = "positions"
    model = models.Position


class PositionCreate(generic.CreateView):
    fields = ("title", "description", "skill")
    model = models.Position

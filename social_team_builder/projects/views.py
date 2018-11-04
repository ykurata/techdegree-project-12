
from itertools import chain
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.decorators import login_required
#from django.shortcuts import get_object_or_404, render


from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views import generic

from . import models
from . import forms


def project_detail(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    positions = models.Position.objects.filter(project__id=pk)

    return render(
        request,
        'projects/project_detail.html',
        {'project': project, 'positions': positions})


def create_project(request, pk=None):
    form = forms.ProjectForm()
    position_formset = forms.PositionInlineFormSet(
        queryset=models.Position.objects.none()
    )

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        position_formset = forms.PositionInlineFormSet(
            request.POST,
            queryset=models.Position.objects.none()
        )

        if form.is_valid() and position_formset.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            position_formset = position_formset.save(commit=False)
            for position in position_formset:
                position.project = project
                position.save()
            return HttpResponseRedirect(reverse("home"))

    return render(request, 'projects/project_form.html', {
        'form': form,
        'position_formset': position_formset
    })



class ProjectList(generic.ListView):
    context_object_name = "projects"
    model = models.Project


class ProjectPositionCreate(generic.CreateView):
    model = models.Project
    fields = ("title", "description", "estimated_time", "requirements")
    sucess_url = reverse_lazy("projects:list")

    def get_context_data(self, **kwargs):
        data = super(ProjectPositionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['positions'] = forms.PositionInlineFormSet(self.request.POST)
        else:
            data['positions'] = forms.PositionInlineFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        positions_formset = context['positions']

        if form.is_valid() and positions_formset.is_valid():
            self.object = form.save(commit=False)
            #self.object = positions_formset.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            for position in positions_formset:
                position.save()
        else:
            context = {'form': form, 'positions_formset': formset}
        return super(ProjectPositionCreate, self).form_valid(form)


class ProjectDetail(generic.DetailView):
    #forms_class = forms.PositionInlineFormSet
    model = models.Project
    #model = models.Position
    """
    def get_context_data(self, **kwargs):
        data = super(ProjectPositionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['positions'] = forms.PositionInlineFormSet(self.request.POST)
        else:
            data['positions'] = forms.PositionInlineFormSet()
        return data
    """

class ProjectUpdate(generic.UpdateView):
    fields = ("title", "description", "estimated_time", "requirements")
    model = models.Project


class PositionList(generic.ListView):
    context_object_name = "positions"
    model = models.Position


class PositionCreate(generic.CreateView):
    fields = ("title", "description", "skill")
    model = models.Position

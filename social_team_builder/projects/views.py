
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from django.shortcuts import get_object_or_404, render


from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from . import models
from . import forms


@login_required
def project_detail(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    positions = models.Position.objects.filter(project__id=pk)

    return render(
        request,
        'projects/project_detail.html',
        {'project': project, 'positions': positions})


@login_required
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


@login_required
def edit_project(request, pk):
    try:
        project = models.Project.objects.get(pk=pk)
    except models.Project.DoesNotExist:
        project=None
    form = forms.ProjectForm(instance=project)
    position_formset = forms.PositionInlineFormSet(
        queryset=models.Position.objects.filter(pk=project.pk)
    )

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, instance=project)
        position_formset = forms.PositionInlineFormSet(
            request.POST,
            queryset=models.Position.objects.filter(pk=project.pk)
        )

        if form.is_valid() and position_formset.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            position_formset = position_formset.save(commit=False)
            for position in position_formset:
                position.project = project
                position.save()
            #return redirect('accounts:profile_detail', pk=request.user.id)
            return HttpResponseRedirect(reverse("home"))

    return render(request, 'projects/project_form.html', {
                'form': form,
                'position_formset': position_formset
            })


@login_required
def apply(request, pk):
    position = get_object_or_404(models.Position, pk=pk)
    try:
        models.Application.objects.get(
            applicant=request.user,
            position=position
        )
    except ObjectDoesNotExist:
        models.Application.objects.create(
            applicant=request.user,
            position=position,
            status="new"
        )
        messages.success(request, "You've applyed to {}!".format(position.title))
        return redirect("projects:project_detail", pk=pk)
    else:
        messages.warning(request, "You've already applyed to this position!")
        return redirect("projects:project_detail", pk=pk)


class ApplicationList(LoginRequiredMixin, generic.ListView):
    context_object_name = "applications"
    model = models.Application


class ApplyProject(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return redirect("projects:project_detail",
                        kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        try:
            position = get_object_or_404(models.Position,
                                    pk=self.kwargs.get('position_pk'))
        except models.Position.DoesNotExist:
            messages.warning(
                self.request,
                "You can't apply to this position!"
            )
        else:
            models.Application.objects.create(
                applicant=self.request.user,
                position=position,
            )
            messages.success(
                self.request,
                "You apply to the position!"
            )
        return super().get(request, *args, **kwargs)


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

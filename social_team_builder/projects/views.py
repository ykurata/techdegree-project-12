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
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from . import models
from . import forms
from accounts.models import Skill



@login_required
def project_detail(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    positions = models.Position.objects.filter(project__id=pk)
    user_applications = models.Application.objects.filter(applicant=request.user)
    application = [app.position.pk
                    for app in user_applications]

    return render(
        request,
        'projects/project_detail.html',
        {'project': project, 'positions': positions, 'application': application})


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
def delete_project(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    project.delete()
    messages.success(request, "{} is deleted.".format(project.title))
    return redirect('home')


@login_required
def apply(request, position_pk, pk):
    position = get_object_or_404(models.Position, pk=position_pk)
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
        messages.success(request, "You've applyed for {}!".format(position.title))
        return HttpResponseRedirect(reverse(
                "projects:project_detail",
                args=[pk]))
    else:
        messages.warning(request, "You've already applyed for this position!")
        return HttpResponseRedirect(reverse(
                "projects:project_detail",
                args=[pk]))


@login_required
def application_list(request):
    applications = models.Application.objects.all()
    projects = models.Project.objects.filter(user=request.user)
    return render(request, 'projects/application_list.html',
                {'applications': applications, 'projects': projects })


def accept_application(request, pk):
    application = get_object_or_404(models.Application, pk=pk)
    application.status = "accept"
    application.position.status = True
    application.save()
    models.Notification.objects.create(
        user=application.applicant,
        application=application,
        message="Your application for {} is approved.".format(
                                                    application.position)
    )
    return redirect("projects:application")


def reject_application(request, pk):
    application = get_object_or_404(models.Application, pk=pk)
    application.status = "reject"
    application.save()
    models.Notification.objects.create(
        user=application.applicant,
        application=application,
        message="Your application for {} is rejected.".format(
                                                    application.position)
    )
    return redirect("projects:application")


def notification(request):
    try:
        notifications = models.Notification.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        messages.warning(request, "There is no notification.")
    else:
        return render(request, "projects/notification.html",
                    {'notifications': notifications })

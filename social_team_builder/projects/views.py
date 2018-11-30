from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from . import models
from . import forms
from accounts.models import Skill



@login_required
def project_detail(request, pk):
    """Show project detail"""
    project = get_object_or_404(models.Project, pk=pk)
    positions = models.Position.objects.filter(project_id=pk)

    return render(
        request,
        'projects/project_detail.html', {
        'project': project,
        'positions': positions })


@login_required
def create_project(request, pk=None):
    """Create a new project and positions"""
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
            position_instance = position_formset.save(commit=False)
            for obj in position_formset.deleted_objects:
                obj.delete()
            for position in position_instance:
                position.project = project
                position.save()
            return HttpResponseRedirect(reverse("home"))

    return render(request, 'projects/project_form.html', {
        'form': form,
        'position_formset': position_formset
        })


@login_required
def edit_project(request, pk):
    """Update the project and positions"""
    try:
        project = models.Project.objects.get(pk=pk, user=request.user)
    except ObjectDoesNotExist:
        project = None

    form = forms.ProjectForm(instance=project)
    position_formset = forms.PositionInlineFormSet(
        queryset=models.Position.objects.filter(
            project_id=pk,
            project__user=request.user)
    )

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, instance=project)
        position_formset = forms.PositionInlineFormSet(
            request.POST,
            queryset=models.Position.objects.filter(
                project_id=pk,
                project__user=request.user)
        )

        if form.is_valid() and position_formset.is_valid():
            form.save()
            position_instance = position_formset.save(commit=False)
            for position in position_instance:
                position.project = project
                position.save()
            for position in position_formset.deleted_objects:
                position.delete()
            return HttpResponseRedirect(reverse("home"))

    return render(request, 'projects/project_form.html', {
                'form': form,
                'position_formset': position_formset
            })


@login_required
def confirm_delete(request, pk):
    """Confirm deletion of a project"""
    try:
        project = models.Project.objects.get(pk=pk, user=request.user)
    except ObjectDoesNotExist:
        project = None
    return render(request, 'projects/confirm_delete.html', {'project': project})


@login_required
def delete_project(request, pk):
    """delete a project"""
    try:
        project = models.Project.objects.get(pk=pk, user=request.user)
    except ObjectDoesNotExist:
        project = None
    project.delete()
    messages.success(request, "{} is deleted.".format(project.title))
    return redirect('home')


@login_required
def apply(request, position_pk, pk):
    """Applying for a position"""
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
                kwargs={'pk': pk}))
    else:
        messages.warning(request, "You've already applyed for this position!")
        return HttpResponseRedirect(reverse(
                "projects:project_detail",
                kwargs={'pk': pk}))


@login_required
def application_list(request):
    """Show a list of all applications"""
    applications = models.Application.objects.filter(
            position__project__user=request.user)
    projects = models.Project.objects.filter(user=request.user)
    return render(request, 'projects/application_list.html', {
            'applications': applications,
            'projects': projects })


@login_required
def accept_application_list(request):
    """Show a list of accepted applications"""
    applications = models.Application.objects.filter(
        status="accept",
        position__project__user=request.user)
    projects = models.Project.objects.filter(user=request.user)
    return render(request, 'projects/application_list.html', {
            'applications': applications,
            'projects': projects })


@login_required
def reject_application_list(request):
    """Show a list of rejected applications"""
    applications = models.Application.objects.filter(
        status="reject",
        position__project__user=request.user)
    projects = models.Project.objects.filter(user=request.user)
    return render(request, 'projects/application_list.html', {
            'applications': applications,
            'projects': projects })


@login_required
def new_application_list(request):
    """Show a list of new applied applications"""
    applications = models.Application.objects.filter(
        status="new",
        position__project__user=request.user)
    projects = models.Project.objects.filter(user=request.user)
    return render(request, 'projects/application_list.html', {
            'applications': applications,
            'projects': projects })


def accept_application(request, pk):
    """Accept an application view"""
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
    """Reject an application view"""
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
    """Show notifications for a login user"""
    try:
        notifications = models.Notification.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        messages.warning(request, "There is no notification.")
    else:
        return render(request, "projects/notification.html",
                    {'notifications': notifications })

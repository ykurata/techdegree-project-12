from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from PIL import Image

from projects.models import Position, Project, Application
from . import forms
from . import models


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = 'home'
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
       login(self.request, form.get_user())
       return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


@login_required
def profile_update(request, pk):
    """Update user profile."""
    profile = get_object_or_404(models.User, id=pk)
    form = forms.ProfileForm(instance=profile)
    skill_formset = forms.SkillInlineFormSet(
        queryset=models.Skill.objects.filter(user_id=pk)
        #queryset=form.instance.skill_set.all()
    )

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        skill_formset = forms.SkillInlineFormSet(
            request.POST,
            queryset=models.Skill.objects.filter(user_id=pk)
            )

        if form.is_valid() and skill_formset.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            skill_instance = skill_formset.save(commit=False)
            for obj in skill_formset.deleted_objects:
                obj.delete()
            for skill in skill_instance:
                skill.user=request.user
                skill.save()
            return redirect('accounts:profile_detail', pk=request.user.id)

    return render(request, 'accounts/user_form.html', {
                'form': form,
                'skill_formset': skill_formset })


@login_required
def profile_detail(request, pk):
    """Show user's profile detail, skills, projects, and applyed projects"""
    profile = get_object_or_404(models.User, pk=pk)
    skills = models.Skill.objects.filter(user_id=pk)
    projects = Project.objects.filter(user_id=pk)
    applications = Application.objects.filter(
                        applicant=request.user,
                        status='accept')
    return render(request, 'accounts/profile_detail.html', {
            'profile': profile,
            'skills': skills,
            'projects': projects ,
            'applications': applications })

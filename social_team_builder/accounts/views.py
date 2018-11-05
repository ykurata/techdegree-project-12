from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from PIL import Image


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


class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.ProfileForm
    model = models.User

    def get_success_url(self):
        return reverse('accounts:profile_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['skills'] = forms.SkillInlineFormSet(self.request.POST)
        else:
            context['skills'] = forms.SkillInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        skills_formset = context['skills']
        if form.is_valid() and skills_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            for skill in skills_formset:
                skill.save()
        else:
            context = {'form': form, 'skills_formset': skills_formset}
        return super(ProfileUpdate, self).form_valid(form)

def profile_update(request, pk):
    try:
        profile = models.User.objects.get(id=pk)
    except models.User.DoesNotExist:
        profile=None
    form = forms.ProfileForm(instance=profile)
    skill_formset = forms.SkillInlineFormSet(
        queryset=models.User.objects.none()
    )

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        skill_formset = forms.SkillInlineFormSet(
            request.POST,
            queryset=models.User.objects.none()
        )

        if form.is_valid() and skill_formset.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            skill_formset = skill_formset.save(commit=False)
            for skill in skill_formset:
                skill.user = request.user
                skill.save()

            return redirect('accounts:profile_detail', pk=request.user.id)
    return render(request, 'accounts/user_form.html', {
                'form': form,
                'skill_formset': skill_formset })


def profile_detail(request, pk):
    #profile = models.User.objects.get(id=pk)
    profile = get_object_or_404(models.User, pk=pk)
    skills = models.Skill.objects.filter(user=request.user)
    return render(request, 'accounts/profile_detail.html', {
            'profile': profile, 'skills': skills })


class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = models.User
    fields = ("image", "bio", "skill")
    template_name = "accounts/profile_detail.html"

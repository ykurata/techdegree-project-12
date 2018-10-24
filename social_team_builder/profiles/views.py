from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.core.urlresolvers import reverse_lazy

#from django.http import HttpResponse
from django.views import generic

from . import models
from . import forms


class ProfileCreate(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ProfileForm
    model = models.Profile
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Profile


class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    fields = ('image', 'bio', 'skill')
    model = models.Profile

    def get_success_url(self):
        user_id = self.kwargs['pk']
        return reverse_lazy("profiles:profile_detail", kwargs={'pk':user_id})

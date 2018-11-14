from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from projects.models import Project, Position


class Home(ListView):
    model = Project
    template_name = "home.html"

    def get_queryset(self):
        return Project.objects.all().prefetch_related('positions')

    """
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['position_list'] = Position.objects.all()
        return context
    """

def home(request):
    projects = Project.objects.prefetch_related('position')

    return render(request, 'home.html',
                {'projects': projects})

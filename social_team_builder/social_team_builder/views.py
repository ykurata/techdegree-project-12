from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from projects.models import Project, Position


class Home(ListView):
    model = Project
    template_name = "home.html"

    def get_queryset(self):
        term = self.request.GET.get('q', '')
        if term:
            return Project.objects.filter(
                Q(title__icontains=term) | Q(description__icontains=term)
            )
        else:
            return Project.objects.all()

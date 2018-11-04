from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from projects.models import Project, Position


class Home(TemplateView):
    template_name = "index.html"


def home(request):
    positions = Position.objects.all()
    return render(request, 'home.html', {'positions': positions})

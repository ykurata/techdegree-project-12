from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.ProjectList.as_view(), name="list"),

    url(r"^(?P<pk>\d+)/$",
        views.project_detail,
        name="project_detail"),

    url(r"^create_project/$",
        views.create_project,
        name="create"),
]

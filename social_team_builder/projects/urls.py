from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.ProjectList.as_view(), name="list"),

    url(r"^create_project/$",
        views.ProjectPositionCreate.as_view(),
        name="create_project"),

    url(r"^(?P<pk>\d+)/$",
        views.ProjectDetail.as_view(),
        name="project_detail"),

    url(r"^(?P<pk>\d+)/edit/$",
        views.ProjectUpdate.as_view(),
        name="project_update"),

    url(r"^(?P<pk>\d+)/edit/$",
        views.ProjectUpdate.as_view(),
        name="project_update"),

    url(r"^create_position/$",
        views.PositionCreate.as_view(),
        name="create_position"),
]

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^(?P<pk>\d+)/$", views.project_detail, name="project_detail"),

    url(r"^create_project/$", views.create_project, name="create"),

    url(r"^(?P<pk>\d+)/edit/$", views.edit_project, name="project_edit"),

    #url(r"^(?P<pk>\d+)/apply/$", views.ApplyProject.as_view(), name="apply"),
    url(r"^(?P<pk>\d+)/apply/$", views.apply, name="apply"),

]

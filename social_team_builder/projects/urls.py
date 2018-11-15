from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^(?P<pk>\d+)/$", views.project_detail, name="project_detail"),

    url(r"^create_project/$", views.create_project, name="create"),

    url(r"^(?P<pk>\d+)/edit/$", views.edit_project, name="project_edit"),

    url(r"^(?P<pk>\d+)/apply/$", views.apply, name="apply"),

    #url(r"search/$", views.search, name="search"),

    url(r"^application/$",
        views.application_list,
        name="application"),

    url(r"^application/(?P<pk>\d+)/accept/$",
        views.accept_application,
        name="accept"),

    url(r"^application/(?P<pk>\d+)/reject/$",
        views.reject_application,
        name="reject"),

    url(r"^notification/$",
        views.notification,
        name="notification")
]

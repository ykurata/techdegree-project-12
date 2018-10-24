from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/edit/$',
        views.ProfileUpdate.as_view(), name="profile_update"),
    url(r'^(?P<pk>\d+)/$',
        views.ProfileDetail.as_view(), name="profile_detail"),
    url(r"create_profile/$",
        views.ProfileCreate.as_view(), name="profile_create"),
]

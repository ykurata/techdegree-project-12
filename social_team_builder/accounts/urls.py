from django.conf.urls import url

from . import views

urlpatterns =[
    #url(r'signin/$', views.SigninView.as_view(), name="signin"),
    url(r'logout/$', views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    url(r"edit/(?P<pk>\d+)/$", views.ProfileUpdate.as_view(), name="edit"),
    url(r"profile/(?P<pk>\d+)/$",
        views.ProfileDetail.as_view(),
        name="profile_detail"),
]

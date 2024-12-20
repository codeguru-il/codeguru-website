from django.urls import include, path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/", views.group, name="group"),
    path("group/<int:id>", views.group, name="group"),
    path("center/create", views.new_center, name="new_center"),
    path("center/<str:tkr>", views.center, name="center"),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/profile/delete", views.delete_profile, name="delete_profile"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("invite/create", views.create_invite, name="invite_create"),
    path("invite/<str:code>", views.invite, name="invite"),
    path("invite/", RedirectView.as_view(pattern_name="index", permanent=True)),
    path("group/leave", views.leave_group, name="leave_group"),
    path("set_lang", views.set_lang, name="set_language"),
]

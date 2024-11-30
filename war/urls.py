from django.urls import path

from . import views

urlpatterns = [
    path("", views.challenges, name="challenges"),
    path("riddles/<int:id>", views.riddle_page, name="riddle_page"),
    path("wars/<int:id>", views.war_page, name="war_page"),
    path("wars/<int:id>/download/<str:fieldname>", views.download_war, name="war_download"),
    path("riddles/<int:id>/download", views.download_riddle, name="riddle_download"),
    path("validate_survivor", views.survivor_validator_page, name="validate_survivor"),
]

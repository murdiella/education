from django.urls import path

from . import views

app_name = "applicants"

urlpatterns = [
    path("citizenship/", views.citizenship, name="citizenship"),
    path("personal/", views.personal, name="personal"),
    path("educations/", views.educations, name="educations"),
    path("exams/", views.exams, name="exams"),
    path("preliminary/", views.preliminary, name="preliminary"),
    path(
        "specialities/",
        views.selected_specialities,
        name="selected_specialities",
    ),
    path("", views.root, name="root"),
]

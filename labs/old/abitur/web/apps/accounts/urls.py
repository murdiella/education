from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("manage/", views.access, name="access"),
    path("manage/signup/", views.signup, name="signup"),
    path("confirm/<str:token>/", views.confirm, name="confirm"),
    path("logout/", views.logout, name="logout"),
    path("reconfirm/", views.reconfirm, name="reconfirm"),
    path("forgot/", views.forgot, name="forgot"),
    path("reset/<str:token>/", views.reset, name="reset"),
]

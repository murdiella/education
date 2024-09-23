from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated and request.user.is_confirmed:
        return redirect("applicants:root")
    return redirect(reverse("accounts:login"))

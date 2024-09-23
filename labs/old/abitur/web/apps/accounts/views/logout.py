from django.contrib.auth import logout as auth_logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    return redirect("accounts:login")

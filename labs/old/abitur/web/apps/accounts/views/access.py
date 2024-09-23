from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def access(request: HttpRequest) -> HttpResponse:
    return render(request, "access.html")

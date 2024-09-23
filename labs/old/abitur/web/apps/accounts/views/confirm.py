from apps.accounts.models import SignupToken
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect


def confirm(request: HttpRequest, token: str) -> HttpResponse:
    token_obj = get_object_or_404(SignupToken, token=token)
    user = token_obj.user
    user.confirm_email()
    token_obj.delete()
    login(
        request,
        user=user,
    )
    return redirect("root")

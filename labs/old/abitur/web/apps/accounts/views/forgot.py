from apps.accounts.forms import ForgotForm
from apps.accounts.models import ResetToken
from apps.accounts.services import reset
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, reverse

User = get_user_model()


def forgot(request: HttpRequest) -> HttpResponse:
    form = ForgotForm()
    if request.method == "POST":
        form = ForgotForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                reset(user, url_builder=request.build_absolute_uri)
            return render(request, "reset_email.html", {"email": email})
    return render(
        request,
        "forgot.html",
        {
            "form": form,
        },
    )

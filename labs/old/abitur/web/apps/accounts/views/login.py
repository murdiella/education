from apps.accounts.forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("root")
    form = LoginForm()
    show_reconfirm_link = False
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                # TODO this should be only the case for Model Auth Backend
                if not user.is_confirmed:
                    show_reconfirm_link = True
                else:
                    auth_login(request, user)
                    return redirect("/")
            else:
                messages.error(
                    request, "Неверное имя пользователя или пароль."
                )

    return render(
        request,
        "login.html",
        {
            "form": form,
            "reconfirm": show_reconfirm_link,
        },
    )

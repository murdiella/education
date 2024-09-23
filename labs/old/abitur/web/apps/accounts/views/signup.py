from apps.accounts.forms import SignupForm
from apps.accounts.services import signup as signup_service
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

User = get_user_model()


def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("root")
    form = SignupForm()
    form.fields["email"].label = "E-mail"
    form.fields["password"].label = "Пароль"
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data["email"]
            password = data["password"]
            try:
                signup_service(
                    email=email,
                    password=password,
                    url_builder=request.build_absolute_uri,
                )
            except ValidationError:
                form.add_error(
                    "email", "Пользователь с таким email уже существует"
                )
            else:
                return render(request, "confirm_email.html", {"email": email})
    return render(request, "signup.html", {"form": form})

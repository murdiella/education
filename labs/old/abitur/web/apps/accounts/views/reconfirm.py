from apps.accounts.forms import ReconfirmForm
from apps.accounts.models import SignupToken
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

User = get_user_model()


def reconfirm(request: HttpRequest) -> HttpResponse:
    form = ReconfirmForm()
    if request.method == "POST":
        form = ReconfirmForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            token, created = SignupToken.objects.get_or_create(user=user)
            # TODO fix this
            return send_confirmation(request, user, token)
    return render(request, "reconfirm.html", {"form": form})

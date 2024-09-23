from apps.accounts.forms import ResetForm
from apps.accounts.models import ResetToken
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def reset(request: HttpRequest, token) -> HttpResponse:
    try:
        token_obj = ResetToken.objects.get(token=token)
    except ResetToken.DoesNotExist:
        return HttpResponse("Токен сброса пароля недействителен.", status=404)
    form = ResetForm()
    email = token_obj.user.email
    if request.method == "POST":
        data = {"password": request.POST["password"], "token": token}
        form = ResetForm(data=data)
        form.token = token
        if form.is_valid():
            form.save()
            user = authenticate(
                username=email,
                password=request.POST["password"],
            )
            if user is not None:
                login(
                    request,
                    user=user,
                )
            return redirect("/")
    return render(
        request,
        "reset.html",
        {
            "form": form,
            "email": email,
            "token": token,
        },
    )

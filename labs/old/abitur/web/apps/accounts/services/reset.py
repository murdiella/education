from typing import Callable

from apps.accounts.models import ResetToken
from apps.core.services import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

User = get_user_model()


def reset(
    user: User,
    url_builder: Callable,
):
    user.set_unusable_password()

    user.save()
    token = _get_or_create_reset_token(user)
    _send_reset_email(user, token, url_builder)


def _get_or_create_reset_token(user):
    try:
        token_obj = ResetToken.objects.get(user=user)
    except ResetToken.DoesNotExist:
        token_obj = ResetToken(
            user=user,
        )
        token_obj.full_clean()
        token_obj.save()
    return token_obj.token


def _send_reset_email(user, token, url_builder):

    email = user.email
    url = url_builder(reverse("accounts:reset", kwargs={"token": token}))
    send_mail(
        email,
        "email/signup",
        "Сброс пароля на сайте lk.mai.ru",
        email=email,
        url=url,
    )

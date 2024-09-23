from typing import Callable

from apps.accounts.models import SignupToken
from apps.core.services import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

User = get_user_model()


def signup(
    email: str,
    password: str,
    url_builder: Callable,
) -> (User, SignupToken):
    """Sign up a user with their email and password."""
    user = User(
        email=email,
    )
    user.set_password(password)
    user.full_clean()
    user.save()
    token = _create_signup_token(user)
    _send_confirmation(user, token, url_builder)
    return user, token


def _create_signup_token(user: User) -> SignupToken:
    """Create a sign up token for newly created user."""
    token = SignupToken(
        user=user,
    )
    token.full_clean()
    token.save()
    return token


def _send_confirmation(
    user: User,
    token: SignupToken,
    url_builder: Callable,
):
    email = user.email
    token_value = token.token
    url = url_builder(
        reverse("accounts:confirm", kwargs={"token": token_value})
    )
    send_mail(
        email,
        "email/signup",
        "Подтверждение аккаунта на сайте lk.mai.ru",
        email=email,
        url=url,
    )

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import ResetToken, SignupToken
from .services import signup as signup_service

User = get_user_model()


EMPTY_EMAIL_ERROR = "Необходимо указать email."
EMPTY_PASSWORD_ERROR = "Необходимо указать пароль."


class ExistingUserEmailValidator:
    def __call__(self, email):
        email = email.lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Неверное имя пользователя или пароль.")
        return email


class NotConfirmedEmailValidator(ExistingUserEmailValidator):
    def __call__(self, email):
        email = super().__call__(email)
        user = User.objects.get(email=email)
        if user.is_confirmed:
            raise ValidationError("Has been confirmed already")
        return email


class ConfirmedUserEmailValidator(ExistingUserEmailValidator):
    def __call__(self, email):
        email = super().__call__(email)
        user = User.objects.get(email=email)
        if not user.is_confirmed:
            raise ValidationError("Аккаунт не был подтвержден")
        return email


class ExistingResetTokenValidator:
    def __call__(self, token):
        try:
            ResetToken.objects.get(token=token)
        except ResetToken.DoesNotExist:
            raise ValidationError("Token does not exist")
        return token


class LoginForm(forms.Form):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "E-mail",
                "class": "form__input",
            }
        ),
        validators=[
            ExistingUserEmailValidator(),
            ConfirmedUserEmailValidator(),
        ],
    )
    error_messages = {
        "email": {
            "required": EMPTY_EMAIL_ERROR,
        }
    }
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введите пароль",
                "class": "form__input",
            },
        ),
    )


class SignupForm(forms.Form):

    email = forms.EmailField(
        required=True,
        widget=forms.fields.EmailInput(
            attrs={
                "placeholder": "Введите email",
            }
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введите пароль",
            }
        ),
        validators=[validate_password],
    )

    class Meta:
        fields = ("email", "password")
        fields_required = ("email", "password")
        error_messages = {
            "email": {"required": EMPTY_EMAIL_ERROR},
            "password": {"required": EMPTY_PASSWORD_ERROR},
        }


class ReconfirmForm(forms.Form):

    email = forms.EmailField(
        required=True,
        validators=[
            NotConfirmedEmailValidator(),
        ],
    )
    error_messages = {
        "email": {
            "required": EMPTY_EMAIL_ERROR,
        }
    }

    def save(self, *args, **kwargs):
        # TODO remove this method from the codebase
        ...


class ForgotForm(forms.Form):

    email = forms.EmailField(
        required=True,
        validators=[],
    )
    error_messages = {
        "email": {
            "required": EMPTY_EMAIL_ERROR,
        }
    }

    def save(self, *args, **kwargs):
        # TODO remove this method from the codebase
        ...


class ResetForm(forms.Form):
    token = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),
        max_length=2048,
        validators=[
            ExistingResetTokenValidator(),
        ],
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введите пароль",
            }
        ),
        validators=[validate_password],
    )

    def save(self):
        if not self.is_valid():
            return
        token = ResetToken.objects.get(token=self.cleaned_data["token"])
        user = token.user
        user.set_password(self.cleaned_data["password"])
        user.save()
        token.delete()

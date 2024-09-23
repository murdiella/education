import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.utils import timezone

from .managers import AbitUserManager


class AbitUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField("email address", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"

    objects = AbitUserManager()

    def __str__(self):
        return self.email

    @property
    def username(self):
        return self.email

    @username.setter
    def username(self, value):
        self.email = value

    def set_password(self, raw_password):
        validate_password(raw_password)
        super().set_password(raw_password)

    def confirm_email(self):
        self.is_confirmed = True
        self.save()


def default_token():
    return uuid.uuid4().hex


class AbstractUserToken(models.Model):

    token = models.CharField(
        default=default_token,
        editable=False,
        unique=True,
        max_length=2048,
    )
    user = models.OneToOneField(
        get_user_model(),
        null=False,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        primary_key=True,
    )

    def __str__(self):
        model_name = self._meta.verbose_name
        return f"{model_name}(user={self.user}, token={self.token})"

    class Meta:
        abstract = True


class SignupToken(AbstractUserToken):
    class Meta:
        verbose_name = "Signup token"
        verbose_name_plural = "Signup tokens"


class ResetToken(AbstractUserToken):
    class Meta:
        verbose_name = "Password reset token"
        verbose_name_plural = "Password reset tokens"

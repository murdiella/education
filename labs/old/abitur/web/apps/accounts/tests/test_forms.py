import uuid

from apps.accounts.forms import ReconfirmForm, ResetForm, SignupForm
from apps.accounts.models import ResetToken, SignupToken
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestReconfirmForm(TestCase):
    def test_form_is_invalid_if_there_is_no_user_with_such_email(self):
        form = ReconfirmForm(
            data={
                "email": "valid@email.com",
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_is_valid_if_there_is_non_confirmed_user_with_such_email(
        self,
    ):
        email = "valid@email.com"
        password = "correct horse battery staple"
        User.objects.create(
            email=email,
            password=password,
        )

        form = ReconfirmForm(
            data={
                "email": email,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_if_there_is_confirmed_user_with_such_email(self):
        email = "valid@email.com"
        password = "correct horse battery staple"
        User.objects.create(
            email=email,
            password=password,
            is_confirmed=True,
        )

        form = ReconfirmForm(
            data={
                "email": email,
            }
        )
        self.assertFalse(form.is_valid())

    def test_should_not_create_token_if_there_were_none(self):
        self.assertIsNone(SignupToken.objects.first())
        form = ReconfirmForm(
            data={
                "email": "valid@email.com",
            }
        )
        form.save()
        self.assertIsNone(SignupToken.objects.first())

    def test_should_not_recreate_token_if_there_were_one(self):
        email = "valid@email.com"
        password = "correct horse battery staple"
        user = User.objects.create(
            email=email,
            password=password,
        )
        token = SignupToken.objects.create(user=user)
        old_uuid = token.token
        form = ReconfirmForm(
            data={
                "email": email,
            }
        )
        form.save()
        token = SignupToken.objects.get(user=user)
        self.assertEqual(token.token, old_uuid)


class TestResetForm(TestCase):
    def test_form_is_invalid_for_non_existing_token(self):
        token = uuid.uuid4()
        form = ResetForm(
            data={
                "token": token,
                "password": "new absolutely valid password",
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_is_valid_for_existing_token(self):
        email = "valid@email.com"
        password = "correct horse battery staple"
        user = User.objects.create(
            email=email,
            password=password,
        )
        token = ResetToken.objects.create(user=user)
        form = ResetForm(
            data={
                "token": token.token,
                "password": "new absolutely valid password",
            }
        )
        self.assertTrue(form.is_valid())

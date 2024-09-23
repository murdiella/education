import uuid

from apps.accounts.models import SignupToken
from django.contrib.auth import get_user_model
from django.db.transaction import TransactionManagementError
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class TestSignupToken(TestCase):
    def test_impossible_to_create_two_tokens_for_user(self):
        user = User.objects.create_user(
            email="valid@email.com",
            password="correct horse battery staple",
        )
        SignupToken.objects.create(user=user)
        with self.assertRaises(IntegrityError):
            SignupToken.objects.create(user=user)

    def test_impossible_create_identical_tokens(self):
        user1 = User.objects.create_user(
            email="one@email.com",
            password="correct horse battery staple",
        )
        user2 = User.objects.create_user(
            email="another@email.com",
            password="correct horse battery staple",
        )
        token = uuid.uuid4()
        SignupToken.objects.create(user=user1, token=token)
        with self.assertRaises(IntegrityError):
            SignupToken.objects.create(user=user2, token=token)

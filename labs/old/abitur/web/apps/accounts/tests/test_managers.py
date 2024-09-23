from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class TestAbitUserManager(TestCase):
    def test_create_user_with_valid_email(self):
        user = User.objects.create_user(
            email="valid@email.com", password="correct horse battery staple"
        )
        self.assertEqual(user.email, "valid@email.com")

    def test_username_is_set_to_email(self):
        user = User.objects.create_user(
            email="valid@email.com", password="correct horse battery staple"
        )
        self.assertEqual(user.username, "valid@email.com")

    def test_email_normalization(self):
        user = User.objects.create_user(
            email="VaLiD@eMaIl.cOm", password="correct horse battery staple"
        )
        self.assertEqual(user.username, "valid@email.com")

    def test_impossible_to_create_users_with_same_email(self):
        User.objects.create_user(
            email="VaLiD@eMaIl.cOm", password="correct horse battery staple"
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="VaLiD@eMaIl.cOm",
                password="correct horse battery staple",
            )

    def test_impossible_to_create_user_without_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

    def test_impossible_to_create_user_without_password(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(email="valid@email.com")

    def test_impossible_to_create_user_with_invalid_password(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="valid@email.com", password="qwerty"
            )

    def test_check_password_returns_true_on_same_password(self):
        user = User.objects.create_user(
            email="VaLiD@eMaIl.cOm", password="correct horse battery staple"
        )
        self.assertTrue(user.check_password("correct horse battery staple"))

    def test_check_password_returns_false_on_other_password(self):
        user = User.objects.create_user(
            email="VaLiD@eMaIl.cOm", password="correct horse battery staple"
        )
        self.assertFalse(user.check_password("correct horse battery staple!"))

    def test_possible_to_authenticate_user_via_password(self):
        email = "valid@email.com"
        password = "correct horse battery staple"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user, authenticate(username=email, password=password))

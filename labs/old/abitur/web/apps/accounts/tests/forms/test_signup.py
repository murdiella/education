import pytest
from apps.accounts.forms import ReconfirmForm, ResetForm, SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data",
    [
        {
            "email": "invalid_email",
        },
        {
            "email": "valid@email.com",
        },
    ],
)
def test_signup_form_is_invalid_with_invalid_data(data):
    form = SignupForm(data=data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_signup_form_is_valid_with_valid_data():
    data = {
        "email": "valid@email.com",
        "password": "correct horse battery staple",
    }
    form = SignupForm(data=data)
    assert form.is_valid()


# test signup form is invalid for existent user

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def logged_in_user(client):
    user = User.objects.create_user(
        email="valid@email.com",
        password="secure-password",
        is_confirmed=True,
    )
    client.force_login(user)
    return user

import pytest
from django.urls import reverse


def test_anonymous_user_is_redirected_to_login_page(client):
    url = reverse("root")
    expected_url = reverse("accounts:login")

    response = client.get(url, follow=True)
    url, status_code = response.redirect_chain[-1]

    assert status_code == 302
    assert url == expected_url


@pytest.mark.django_db
def test_logged_in_user_is_redirected_to_citizenship_page(
    client,
    logged_in_user,
):
    url = reverse("root")
    expected_url = reverse("applicants:citizenship")

    response = client.get(url, follow=True)
    _, status_code = response.redirect_chain[-1]
    # Note: applications page can be not last in
    # the redirection chain
    urls = [item[0] for item in response.redirect_chain]

    assert status_code == 302
    assert expected_url in urls

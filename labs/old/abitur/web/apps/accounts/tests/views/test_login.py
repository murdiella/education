from django.urls import reverse


def test_login_view_uses_login_template(client):
    url = reverse("accounts:login")
    response = client.get(url)
    templates = (template.name for template in response.templates)
    assert "login.html" in templates


# test login with invalid email

# test login with invalid password

# test valid user can login login

# test redirected to the root after logen

# test logged in user is redirected to the root

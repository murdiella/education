from behave import when


@when("I visit {url}")
def step_implementation(context, url):
    if url == "my reset password link":
        token = context.user.password_reset_token
        url = f"/accounts/reset/{token}/"
    actual_url = context.url_helper(url)
    context.browser.get(actual_url)
    context.url = actual_url

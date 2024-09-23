import re
from behave import then


@then("a letter with reset password token is sent to user")
def step_implementation(context):
    email = context.user.email
    mail = context.mailbox.get_last_email(email)
    match = re.search("http://webserver/accounts/reset/.+?/", mail.text)
    assert match is not None
    match = re.search("http://webserver/accounts/reset/.+?/", mail.html)
    assert match is not None


@then("a letter with reset password token was not sent to user")
def step_implementation(context):
    email = context.user.email
    mail = context.mailbox.get_last_email(email)
    assert mail is None

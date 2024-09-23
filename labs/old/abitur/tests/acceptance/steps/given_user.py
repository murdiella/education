from behave import given
from selenium.common.exceptions import NoSuchElementException

from tests.acceptance.steps.utils.users import (ApplicantWithCitizenship,
                                                ApplicantWithoutCitizenship,
                                                LoggedInUser, LoggedOutUser,
                                                PasswordResetUser,
                                                UnconfirmedUser, User)


@given("{username} user")
def step_implementation(context, username):
    if username == "anonymous":
        user = User(context)
    elif username == "logged in":
        user = LoggedInUser(context)
    elif username == "logged out":
        user = LoggedOutUser(context)
    elif username == "unconfirmed":
        user = UnconfirmedUser(context)
    context.user = user


@given("user that has requested password reset")
def step_implementation(context):
    context.user = PasswordResetUser(context)


@given('user that is "{type_of_user}"')
def step_implementation(context, type_of_user):
    if type_of_user == "applicant without citizenship":
        user = ApplicantWithoutCitizenship(context)
    elif type_of_user == "applicant with citizenship":
        user = ApplicantWithCitizenship(context)
    context.user = user


def _login(context, email):
    url = context.url_helper("/accounts/login/")
    context.browser.get(url)
    email_field = context.browser.find_element_by_name("email")
    email_field.send_keys(email)
    password_field = context.browser.find_element_by_name("password")
    password_field.send_keys("secure password")
    text = "Войти"
    try:
        element = context.browser.find_element_by_partial_link_text(text)
    except NoSuchElementException:
        try:
            element = context.browser.find_element_by_xpath(
                f'//button[normalize-space()="{text}"]'
            )
        except NoSuchElementException:
            element = context.browser.find_element_by_xpath(
                f'//input[@value="{text}"][@type="submit"]'
            )
    element.click()

import re
import requests
from selenium.common.exceptions import NoSuchElementException

from .logged_out_user import LoggedOutUser


class PasswordResetUser(LoggedOutUser):

    def __init__(self, context, email=None, password=None):
        super().__init__(context, email, password)
        browser = context.browser
        url = context.url_helper("/accounts/forgot/")
        browser.get(url)
        browser_field = context.browser.find_element_by_name("email")
        browser_field.send_keys(self.email)
        text = "Сбросить пароль"
        try:
            element = browser.find_element_by_partial_link_text(text)
        except NoSuchElementException:
            try:
                element = browser.find_element_by_xpath(f'//button[normalize-space()="{text}"]')
            except NoSuchElementException:
                element = browser.find_element_by_xpath(f'//input[@value="{text}"][@type="submit"]')
        element.click()
        if context.environment == "production":
            text = self.context.mailbox.get_last_email(self.email).text
            match = re.search(r"http://webserver/accounts/reset/(.+?)/", text)
            if match:
                token = match.group(1)
        else:
            from apps.accounts.models import ResetToken
            token = ResetToken.objects.get(user__email=self.email).token
        self.password_reset_token = token

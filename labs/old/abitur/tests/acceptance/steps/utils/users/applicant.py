from selenium.common.exceptions import NoSuchElementException

from .logged_in_user import LoggedInUser


class Applicant(LoggedInUser):

    email: str
    password: str

    def __init__(self, context, email=None, password=None):
        super().__init__(context, email, password)
        self.go_home()

    def set_citizenship(self, citizenship):
        browser = self.context.browser
        url = self.context.url_helper("/applicants/citizenship/")
        browser.get(url)
        if citizenship == "Российская Федерация":
            text = "Подать заявление"
            try:
                element = browser.find_element_by_partial_link_text(text)
            except NoSuchElementException:
                try:
                    element = browser.find_element_by_xpath(f'//button[normalize-space()="{text}"]')
                except NoSuchElementException:
                    element = browser.find_element_by_xpath(f'//input[@value="{text}"][@type="submit"]')
            element.click()
        else:
            # click button
            # select
            # click button
            ...

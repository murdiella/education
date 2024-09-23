import secrets
import re

from selenium.common.exceptions import NoSuchElementException


class Person:

    def __init__(self):
        self.lastname = "Иванов"
        self.firstname = "Иван"
        self.middlename = "Иванович"
        self.date_of_birth = "01.01.1990"
        self.place_of_birth = "г. Москва"
        self.gender = "1"


class Passport:

    def __init__(self):
        self.series = "12 34"
        self.number = "123 456"
        self.issued_date = "01.01.2000"
        self.issuer_code = "123-456"
        self.issuer = "ГУВД Москвы"


class Address:

    # TODO generate data with faker
    def __init__(self):
        self.region = "Москва"
        self.district = "Район"
        self.city = "Москва"
        self.township = "Москва"
        self.zipcode = "123456"
        self.street = "Улица"
        self.house = "Дом"
        self.building = "1"
        self.apartment = "2"


class Contacts:

    def __init__(self):
        self.phone = "12345678900"


class User:

    email: str
    password: str
    personal: Person
    passport: Passport
    address: Address
    contacts: Contacts

    def __init__(self, context, email=None, password=None):
        if email is None:
            email = secrets.token_hex(16) + "@email.com"
        if password is None:
            password = secrets.token_hex(32)
        self.email = email
        self.password = password
        self.context = context
        self.personal = Person()
        self.passport = Passport()
        self.address = Address()
        self.contacts = Contacts()

    def register(self):
        url = self.context.url_helper("/accounts/manage/signup/")
        browser = self.context.browser
        browser.get(url)
        email_field = browser.find_element_by_name("email")
        email_field.send_keys(self.email)
        password_field = browser.find_element_by_name("password")
        password_field.send_keys(self.password)
        text = "Зарегистрироваться"
        try:
            element = browser.find_element_by_partial_link_text(text)
        except NoSuchElementException:
            try:
                element = browser.find_element_by_xpath(
                    f'//button[normalize-space()="{text}"]'
                )
            except NoSuchElementException:
                element = browser.find_element_by_xpath(
                    f'//input[@value="{text}"][@type="submit"]'
                )
        element.click()

    def confirm(self):
        if self.context.environment == "production":
            text = self.context.mailbox.get_last_email(self.email).text
            match = re.search(r"http://webserver/accounts/confirm/.+?/", text)
            if match:
                url = match.group(0)
                self.context.browser.get(url)
            else:
                raise AssertionError("did not match regex for url")
        else:
            from apps.accounts.models import AbitUser

            user = AbitUser.objects.get(email=self.email)
            user.is_confirmed = True
            user.save()
            self.login()

    def login(self):
        url = self.context.url_helper("/accounts/login/")
        browser = self.context.browser
        browser.get(url)
        email_field = browser.find_element_by_name("email")
        email_field.send_keys(self.email)
        password_field = browser.find_element_by_name("password")
        password_field.send_keys(self.password)
        text = "Войти"
        try:
            element = browser.find_element_by_partial_link_text(text)
        except NoSuchElementException:
            try:
                element = browser.find_element_by_xpath(
                    f'//button[normalize-space()="{text}"]'
                )
            except NoSuchElementException:
                element = browser.find_element_by_xpath(
                    f'//input[@value="{text}"][@type="submit"]'
                )
        element.click()

    def go_home(self):
        url = self.context.url_helper("/")
        browser = self.context.browser
        browser.get(url)

    def logout(self):
        url = self.context.url_helper("/accounts/logout/")
        browser = self.context.browser
        browser.get(url)

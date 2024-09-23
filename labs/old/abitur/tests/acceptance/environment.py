import os
import geckodriver_autoinstaller
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from steps.utils.mailbox import Mailbox
from steps.utils.form import FormFiller


def before_all(context):
    environment = os.getenv("DJANGO_ENVIRONMENT", "test").lower()
    context.environment = environment
    context.mailbox = Mailbox(environment)
    if environment == "production":
        from time import sleep

        sleep(60)  # wait for containers to spin up
    else:
        geckodriver_autoinstaller.install()


def before_tag(context, tag):
    if tag == "browser":
        if context.environment == "production":
            host = "selenium-hub"
            port = 4444
            browser = webdriver.Remote(
                command_executor=(f"http://{host}:{port}/wd/hub"),
                desired_capabilities=DesiredCapabilities.FIREFOX,
            )
            context.browser = browser
            context.url_helper = lambda s: f"http://webserver{s}"
        else:
            context.url_helper = lambda s: context.get_url(s)
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            context.browser = webdriver.Firefox(
                firefox_options=options,
            )
        context.form_filler = FormFiller(context.browser)


def after_tag(context, tag):
    if tag == "browser":
        context.browser.quit()


def before_step(context, step):
    if hasattr(context, "browser"):
        body = context.browser.find_element_by_tag_name("body")
        context.page_text = body.text
    else:
        context.page_text = context.stdout_capture
    generate_fixtures(context.environment)


def generate_fixtures(envronment):
    if envronment == "production":
        pass
    else:
        from apps.geography.models import Country

        russia, created = Country.objects.get_or_create(
            ref="0",
            name="Российская Федерация",
            code="643",
        )
        belarus, created = Country.objects.get_or_create(
            ref="1",
            name="Республика Беларусь",
            code="111",
        )

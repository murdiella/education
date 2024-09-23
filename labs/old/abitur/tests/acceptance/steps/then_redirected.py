from urllib.parse import urlparse

from behave import then
from selenium.webdriver.support.ui import WebDriverWait


@then("I should be redirected to {url}")
def step_implementation(context, url):
    wait = WebDriverWait(context.browser, 10)
    expected = context.url_helper(url)
    import time

    time.sleep(10)
    print(context.browser.current_url)
    print(context.browser.page_source)
    wait.until(lambda browser: _path(browser.current_url) == _path(expected))


@then("I should be redirected")
def step_implementation(context):
    url = context.url
    wait = WebDriverWait(context.browser, 10)
    wait.until(lambda browser: _path(browser.current_url) != _path(url))


@then("I should not be redirected")
def step_implementation(context):
    url = context.url
    # TODO reconsider this check into
    # something less naive
    context.browser.implicitly_wait(2)
    assert context.browser.current_url == url


def _path(url):
    return urlparse(url).path

from behave import when
from selenium.common.exceptions import NoSuchElementException


@when("I click \"{text}\"")
def step_implementation(context, text):
    try:
        element = context.browser.find_element_by_partial_link_text(text)
    except NoSuchElementException:
        try:
            element = context.browser.find_element_by_xpath(f'//button[normalize-space()="{text}"]')
        except NoSuchElementException:
            element = context.browser.find_element_by_xpath(f'//input[@value="{text}"][@type="submit"]')
    element.click()

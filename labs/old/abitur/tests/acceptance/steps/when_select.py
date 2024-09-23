from behave import when
from selenium.webdriver.support.select import Select


@when('I select "{value}" as {item}')
def step_implementation(context, value, item):
    browser = context.browser
    select = Select(browser.find_element_by_name(item))
    select.select_by_visible_text(value)

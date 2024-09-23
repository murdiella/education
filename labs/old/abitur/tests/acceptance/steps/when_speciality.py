from behave import when
import random


@when("I select {n} specialities")
def step_implementation(context, n):
    n = int(n)
    for _ in range(n):
        select_unselected_speciality(context.browser)


@when("I select 1 speciality")
def step_implementation(context):
    select_unselected_speciality(context.browser)


def select_unselected_speciality(browser):
    specialities = browser.find_elements_by_css_selector(
        ".speciality-block:not(.active):not(.speciality-block_form-control)",
    )
    speciality = random.choice(specialities)
    speciality.click()

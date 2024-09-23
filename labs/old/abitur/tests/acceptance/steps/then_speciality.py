from behave import then


@then("{n} specialities are selected")
def step_implementation(context, n):
    n = int(n)
    browser = context.browser
    specialities = browser.find_elements_by_css_selector(".speciality-block.active")
    cnt = len(specialities)
    print(cnt)
    assert cnt == n

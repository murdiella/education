from behave import when


@when("I check personal data processing agreement")
def step_implementation(context):
    element = context.browser.find_element_by_id("personal_data_processing_agree_label")
    element.click()

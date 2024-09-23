from behave import then


@then("I should see {value}")
def step_implementation(context, value):
    if value.startswith("my "):
        value = value.removeprefix("my ")
        value = getattr(context.user, value)
    else:
        value = value.strip("\"")
    assert value in context.page_text

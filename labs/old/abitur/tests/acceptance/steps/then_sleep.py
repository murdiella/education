from time import sleep

from behave import then


@then("sleep")
def step_implementation(context):
    sleep(10)

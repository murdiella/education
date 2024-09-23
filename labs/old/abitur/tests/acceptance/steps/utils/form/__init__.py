class FormFiller:

    def __init__(self, browser):
        self.browser = browser

    def fill(self, name, value):
        field = self.browser.find_element_by_name(name)
        if field.get_attribute("type") == "radio":
            field = self.browser.find_element_by_xpath(
                f"//input[@value={value!r} and @type='radio' and @name={name!r}]/..",
            )
            field.click()
        else:
            field.send_keys(value)

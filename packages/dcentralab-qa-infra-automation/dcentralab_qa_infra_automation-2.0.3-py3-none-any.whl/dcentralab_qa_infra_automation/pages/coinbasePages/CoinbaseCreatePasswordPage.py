from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
create password page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
CREATE_PASSWORD_CONTAINER = (By.CSS_SELECTOR, "[data-element-handle='step-password-active']")
PASSWORD_INPUT = (By.ID, "Password")
VERIFY_PASSWORD_INPUT = (By.ID, "Verify password")
AGREE_TERMS_CHECKBOX = (By.CSS_SELECTOR, "#cds-checkbox-input--c1ush59lx7w[data-testid='terms-and-privacy-policy']")
SUBMIT_BUTTON = (By.CSS_SELECTOR, "[data-testid='btn-password-continue']")


class CoinbaseCreatePasswordPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return (self.is_element_exist("CREATE_PASSWORD_CONTAINER", CREATE_PASSWORD_CONTAINER) and
                self.is_element_exist("PASSWORD_INPUT", PASSWORD_INPUT) and
                self.is_element_exist("VERIFY_PASSWORD_INPUT", VERIFY_PASSWORD_INPUT) and
                self.is_element_exist("AGREE_TERMS_CHECKBOX", AGREE_TERMS_CHECKBOX) and
                self.is_element_exist("SUBMIT_BUTTON", SUBMIT_BUTTON))

    def insert_password(self, password):
        """
        insert password
        """
        self.enter_text("PASSWORD_INPUT", PASSWORD_INPUT, password)

    def verify_password(self, password):
        """
        verify password
        """
        self.enter_text("VERIFY_PASSWORD_INPUT", VERIFY_PASSWORD_INPUT, password)

    def click_on_agree_terms_checkbox(self):
        """
        click on agree terms checkbox
        """
        self.click("AGREE_TERMS_CHECKBOX", AGREE_TERMS_CHECKBOX)

    def click_on_submit(self):
        """
        click on submit
        """
        self.click("SUBMIT_BUTTON", SUBMIT_BUTTON)

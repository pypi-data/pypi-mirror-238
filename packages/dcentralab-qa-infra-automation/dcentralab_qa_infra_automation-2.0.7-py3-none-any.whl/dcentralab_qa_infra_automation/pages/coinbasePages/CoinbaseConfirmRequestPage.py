import pytest

from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
confirm request page

@Author: Efrat Cohen
@Date: 03.2023
"""

"""page locators"""
COINBASE_CONNECT_WALLET_TO_APP_CONTAINER = (By.CSS_SELECTOR, "[data-testid='authorization-request-permission-list']")
COINBASE_CONFIRM_BUTTON = (By.CSS_SELECTOR, '[data-testid="allow-authorize-button"]')


class CoinbaseConfirmRequestPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("COINBASE_CONNECT_WALLET_TO_APP_CONTAINER",
                                     COINBASE_CONNECT_WALLET_TO_APP_CONTAINER)

    def click_on_confirm_button(self):
        """
        click on confirm button
        """

        if self.is_element_exist_with_custom_timeout("COINBASE_CONFIRM_BUTTON", COINBASE_CONFIRM_BUTTON,
                                                     pytest.properties.get("timeout") / 10):

            self.click("COINBASE_CONFIRM_BUTTON", COINBASE_CONFIRM_BUTTON)
        else:
            # Close chrome extension popup
            self.driver.close()
            pytest.logger.info("coinbase wallet already connected")

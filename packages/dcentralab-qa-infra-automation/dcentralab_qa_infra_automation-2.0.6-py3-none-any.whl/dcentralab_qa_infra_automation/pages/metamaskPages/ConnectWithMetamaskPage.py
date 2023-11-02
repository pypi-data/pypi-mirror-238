import pytest
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
connect with metamask page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
CONNECT_WALLET_PERMISSIONS_CONTAINER = (By.CLASS_NAME, "permissions-connect")
CONTAINER_TITLE = (By.CLASS_NAME, "permissions-connect-header__title")
NEXT_BUTTON = (By.XPATH, "//button[contains(@class,'btn-primary') and contains(text(),'Next')]")
CONNECT_BUTTON = (By.CSS_SELECTOR, "[data-testid='page-container-footer-next']")
CONNECT_WITH_METAMASK_EXTENSION_BUTTON = (By.XPATH, "//*[contains(text(),'Connect With MetaMask Extension')]")


class ConnectWithMetamaskPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        url = self.driver.current_url
        return "connect" in url and self.is_element_exist("CONNECT_WALLET_PERMISSIONS_CONTAINER",
                                                          CONNECT_WALLET_PERMISSIONS_CONTAINER) and "MetaMask" in self.get_text(
            "CONTAINER_TITLE", CONTAINER_TITLE)

    def click_on_connect_with_metamask_extension_button(self):
        """
        click on connect with metamask extension popup button
        """
        # If the popup exists
        if self.is_element_exist_with_custom_timeout("CONNECT_WITH_METAMASK_EXTENSION_BUTTON",
                                                     CONNECT_WITH_METAMASK_EXTENSION_BUTTON,
                                                     pytest.properties.get("timeout") / 10):
            # Click on the button
            self.click("CONNECT_WITH_METAMASK_EXTENSION_BUTTON", CONNECT_WITH_METAMASK_EXTENSION_BUTTON)
        else:
            return

    def click_on_next_button(self):
        """
        click on next button
        """
        self.click("NEXT_BUTTON", NEXT_BUTTON)

    def click_on_connect_button(self):
        """
        click on connect button
        """
        url = self.driver.current_url
        if "confirm-permissions" in url and "Connect" in self.get_text("CONNECT_BUTTON)", CONNECT_BUTTON):
            self.click("CONNECT_BUTTON", CONNECT_BUTTON)

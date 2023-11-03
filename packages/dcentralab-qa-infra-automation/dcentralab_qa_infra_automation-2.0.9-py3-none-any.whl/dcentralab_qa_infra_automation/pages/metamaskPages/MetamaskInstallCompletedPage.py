from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
metamask install completed page

@Author: Efrat Cohen
@Date: 07.2023
"""

"""page locators"""
METAMASK_INSTALL_COMPLETE_CONTAINER = (By.CLASS_NAME, "onboarding-pin-extension")
METAMASK_PIN_EXTENSION_NEXT_BUTTON = (By.CSS_SELECTOR, "[data-testid='pin-extension-next']")
METAMASK_PIN_EXTENSION_DONE_BUTTON = (By.CSS_SELECTOR, "[data-testid='pin-extension-done']")
METAMASK_WHATS_NEW_POPUP_CONTAINER = (By.CLASS_NAME, "whats-new-popup__popover")
METAMASK_WHATS_NEW_CLOSE_BUTTON = (By.CSS_SELECTOR, "[data-testid='popover-close']")


class MetamaskInstallCompletedPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("METAMASK_INSTALL_COMPLETE_CONTAINER",
                                     METAMASK_INSTALL_COMPLETE_CONTAINER) and self.is_element_exist(
            "METAMASK_PIN_EXTENSION_NEXT_BUTTON", METAMASK_PIN_EXTENSION_NEXT_BUTTON)

    def click_on_next(self):
        """
        click on next button
        """
        self.click("METAMASK_PIN_EXTENSION_NEXT_BUTTON", METAMASK_PIN_EXTENSION_NEXT_BUTTON)

    def is_done_button_exist(self):
        """
        check is Done button exist
        :return: true if existed, otherwise return false
        """
        return self.is_element_exist("METAMASK_PIN_EXTENSION_DONE_BUTTON", METAMASK_PIN_EXTENSION_DONE_BUTTON)

    def click_on_done(self):
        """
        click on done button
        """
        self.click("METAMASK_PIN_EXTENSION_DONE_BUTTON", METAMASK_PIN_EXTENSION_DONE_BUTTON)

    def is_whats_new_popup_loaded(self):
        """
        check is Try it out
        :return: true if existed, otherwise return false
        """
        return self.is_element_exist("METAMASK_WHATS_NEW_POPUP_CONTAINER", METAMASK_WHATS_NEW_POPUP_CONTAINER)

    def close_whats_new_popup(self):
        """
        click on Try it out button
        """
        self.click("METAMASK_WHATS_NEW_CLOSE_BUTTON", METAMASK_WHATS_NEW_CLOSE_BUTTON)

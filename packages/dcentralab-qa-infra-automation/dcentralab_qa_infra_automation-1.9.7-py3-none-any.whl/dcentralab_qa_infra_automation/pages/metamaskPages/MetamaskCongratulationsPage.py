from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
congratulations page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
METAMASK_CONGRATULATIONS_CONTAINER = (By.CLASS_NAME, "creation-successful")
METAMASK_GOT_IT_BUTTON = (By.CSS_SELECTOR, "[data-testid='onboarding-complete-done']")


class MetamaskCongratulationsPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("METAMASK_CONGRATULATIONS_CONTAINER", METAMASK_CONGRATULATIONS_CONTAINER)

    def click_on_got_it_button(self):
        """
        click on got it button
        """
        self.click("METAMASK_GOT_IT_BUTTON", METAMASK_GOT_IT_BUTTON)

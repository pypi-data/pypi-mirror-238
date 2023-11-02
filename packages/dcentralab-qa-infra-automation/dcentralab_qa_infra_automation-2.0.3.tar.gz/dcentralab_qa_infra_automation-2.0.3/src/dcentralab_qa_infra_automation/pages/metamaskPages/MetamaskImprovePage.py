from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
improve metamask page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
METAMASK_IMPROVE_CONTAINER = (By.CSS_SELECTOR, "[data-testid='onboarding-metametrics']")
METAMASK_I_AGREE_BUTTON = (By.CSS_SELECTOR, "[data-testid='metametrics-i-agree']")


class MetamaskImprovePage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("METAMASK_IMPROVE_CONTAINER", METAMASK_IMPROVE_CONTAINER)

    def click_on_i_agree_button(self):
        """
        click on i agree button
        """
        self.click("METAMASK_I_AGREE_BUTTON", METAMASK_I_AGREE_BUTTON)

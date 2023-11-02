from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
allow the site to switch the network page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
METAMASK_SWITCH_NETWORK_CONTAINER_CONTENT = (By.CLASS_NAME, "confirmation-page__content")
METAMASK_SWITCH_NETWORK_CONTAINER_TITLE = (By.CSS_SELECTOR, ".confirmation-page__content h3")
METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON = (
    By.XPATH, "//button[contains(@class,'btn-primary') and contains(text(),'Switch network')]")


class MetamaskSwitchNetworkPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        url = self.driver.current_url
        return \
            ("confirmation" in url and
             self.is_element_exist("METAMASK_SWITCH_NETWORK_CONTAINER_CONTENT",
                                   METAMASK_SWITCH_NETWORK_CONTAINER_CONTENT) and
                "switch" in self.get_text("METAMASK_SWITCH_NETWORK_CONTAINER_TITLE",
                                          METAMASK_SWITCH_NETWORK_CONTAINER_TITLE))

    def click_on_switch_network_button(self):
        """
        click on switch network button
        """
        self.click("METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON", METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON)

from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
receive crypto to your username page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
PORTFOLIO_CONTAINER = (By.CSS_SELECTOR, "[data-testid='portfolio-component']")
ANNOUNCEMENT_MESSAGE_NEW_USER = (By.CSS_SELECTOR, "[data-testid='new-user-subdomain-announcement']")
ANNOUNCEMENT_CLOSE_BUTTON = (By.CSS_SELECTOR, "[data-icon-name='close']")


class CoinbasePortfolioPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        is_page_loaded = False
        if self.is_element_exist("PORTFOLIO_CONTAINER", PORTFOLIO_CONTAINER):
            is_page_loaded = True
            self.close_message_announcement()
        return is_page_loaded

    def close_message_announcement(self):
        if self.is_element_exist("ANNOUNCEMENT_MESSAGE_NEW_USER", ANNOUNCEMENT_MESSAGE_NEW_USER):
            self.click("ANNOUNCEMENT_CLOSE_BUTTON", ANNOUNCEMENT_CLOSE_BUTTON)

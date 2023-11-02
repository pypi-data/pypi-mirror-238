from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
create or import wallet page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
COINBASE_TITLE = (By.CSS_SELECTOR, "[data-testid='warm-welcome-text-animation']")
COINBASE_CREATE_WALLET_BUTTON = (By.CSS_SELECTOR, "[data-testid='btn-create-new-wallet']")
ALREADY_HAVE_WALLET_BTN = (By.CSS_SELECTOR, "[data-testid='btn-import-existing-wallet']")


class CoinbaseCreateWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("COINBASE_TITLE", COINBASE_TITLE) and self.is_element_exist(
            "COINBASE_CREATE_WALLET_BUTTON", COINBASE_CREATE_WALLET_BUTTON) and self.is_element_exist(
            "ALREADY_HAVE_WALLET_LINK", ALREADY_HAVE_WALLET_BTN)

    def click_on_already_have_a_wallet(self):
        """
        click on already have a wallet
        """
        self.click("ALREADY_HAVE_WALLET_LINK", ALREADY_HAVE_WALLET_BTN)

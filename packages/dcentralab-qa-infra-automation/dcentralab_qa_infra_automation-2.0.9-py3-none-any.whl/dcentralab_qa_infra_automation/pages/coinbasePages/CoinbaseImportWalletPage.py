from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
import wallet page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
IMPORT_WALLET_CONTAINER = (By.CSS_SELECTOR, "[data-testid='import-wallet-container']")
IMPORT_WALLET_CONTAINER_TITLE = (By.CSS_SELECTOR, "[data-testid='import-secret']")
SEED_PHRASE_INPUT = (By.NAME, "seed-phrase-input")
IMPORT_WALLET_BTN = (By.CSS_SELECTOR, "[data-testid='btn-import-wallet']")
COINBASE_APP_CONTAINER = (By.ID, "app-main")


class CoinbaseImportWalletPage(BasePage):
    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """

        return self.is_element_exist("IMPORT_WALLET_CONTAINER", IMPORT_WALLET_CONTAINER) and self.is_element_exist(
            "SEED_PHRASE_INPUT", SEED_PHRASE_INPUT)

    def insert_recovery_phrase(self, recovery_phrase):
        """
        enter recovery phrase
        """
        self.enter_text("SEED_PHRASE_INPUT", SEED_PHRASE_INPUT, recovery_phrase)

    def click_on_import_wallet_button(self):
        if self.is_button_enable("IMPORT_WALLET_BTN", IMPORT_WALLET_BTN):
            self.click("IMPORT_WALLET_BTN", IMPORT_WALLET_BTN)

    def is_wallet_imported(self):
        is_imported = self.is_element_exist_with_custom_timeout("COINBASE_APP_CONTAINER", COINBASE_APP_CONTAINER,
                                                                self.timeout - 45)
        return is_imported

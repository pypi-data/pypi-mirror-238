from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
use an existing wallet page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
IMPORT_WALLET_METHOD_CONTAINER = (By.CSS_SELECTOR, "[data-testid='select-import-method-onboarding']")
IMPORT_WALLET_VIA_SEED_PHRASE_BTN = (By.CSS_SELECTOR, "[data-testid='btn-import-recovery-phrase']")


class CoinbaseUseAnExistingWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("IMPORT_WALLET_METHOD_CONTAINER",
                                     IMPORT_WALLET_METHOD_CONTAINER) and self.is_element_exist(
            "IMPORT_WALLET_VIA_SEED_PHRASE_BTN", IMPORT_WALLET_VIA_SEED_PHRASE_BTN)

    def click_on_import_wallet_seed_phrase_method(self):
        """
        click on import wallet through seed phrase
        """
        self.click("IMPORT_WALLET_VIA_SEED_PHRASE_BTN", IMPORT_WALLET_VIA_SEED_PHRASE_BTN)

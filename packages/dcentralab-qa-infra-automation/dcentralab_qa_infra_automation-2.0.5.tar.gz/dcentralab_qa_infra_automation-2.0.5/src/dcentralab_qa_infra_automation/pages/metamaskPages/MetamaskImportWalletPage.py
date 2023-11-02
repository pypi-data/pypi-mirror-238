import pytest
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
import wallet page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
METAMASK_IMPORT_WALLET_SECRET_PHRASE_CONTAINER = (By.CLASS_NAME, "import-srp")
INPUT_SECRET_RECOVERY_PHRASE_0 = (By.ID, "import-srp__srp-word-0")
INPUT_SECRET_RECOVERY_PHRASE_1 = (By.ID, "import-srp__srp-word-1")
INPUT_SECRET_RECOVERY_PHRASE_2 = (By.ID, "import-srp__srp-word-2")
INPUT_SECRET_RECOVERY_PHRASE_3 = (By.ID, "import-srp__srp-word-3")
INPUT_SECRET_RECOVERY_PHRASE_4 = (By.ID, "import-srp__srp-word-4")
INPUT_SECRET_RECOVERY_PHRASE_5 = (By.ID, "import-srp__srp-word-5")
INPUT_SECRET_RECOVERY_PHRASE_6 = (By.ID, "import-srp__srp-word-6")
INPUT_SECRET_RECOVERY_PHRASE_7 = (By.ID, "import-srp__srp-word-7")
INPUT_SECRET_RECOVERY_PHRASE_8 = (By.ID, "import-srp__srp-word-8")
INPUT_SECRET_RECOVERY_PHRASE_9 = (By.ID, "import-srp__srp-word-9")
INPUT_SECRET_RECOVERY_PHRASE_10 = (By.ID, "import-srp__srp-word-10")
INPUT_SECRET_RECOVERY_PHRASE_11 = (By.ID, "import-srp__srp-word-11")
CONFIRM_BUTTON = (By.CLASS_NAME, "import-srp__confirm-button")


class MetamaskImportWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("METAMASK_IMPORT_WALLET_SECRET_PHRASE_CONTAINER",
                                     METAMASK_IMPORT_WALLET_SECRET_PHRASE_CONTAINER)

    def insert_secret_recovery_phrase(self, seed_phrase_0, seed_phrase_1, seed_phrase_2, seed_phrase_3, seed_phrase_4,
                                      seed_phrase_5, seed_phrase_6, seed_phrase_7, seed_phrase_8, seed_phrase_9,
                                      seed_phrase_10, seed_phrase_11):
        """
        insert secret recovery phrase
        """
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_0", INPUT_SECRET_RECOVERY_PHRASE_0, seed_phrase_0)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_1", INPUT_SECRET_RECOVERY_PHRASE_1, seed_phrase_1)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_2", INPUT_SECRET_RECOVERY_PHRASE_2, seed_phrase_2)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_3", INPUT_SECRET_RECOVERY_PHRASE_3, seed_phrase_3)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_4", INPUT_SECRET_RECOVERY_PHRASE_4, seed_phrase_4)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_5", INPUT_SECRET_RECOVERY_PHRASE_5, seed_phrase_5)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_6", INPUT_SECRET_RECOVERY_PHRASE_6, seed_phrase_6)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_7", INPUT_SECRET_RECOVERY_PHRASE_7, seed_phrase_7)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_8", INPUT_SECRET_RECOVERY_PHRASE_8, seed_phrase_8)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_9", INPUT_SECRET_RECOVERY_PHRASE_9, seed_phrase_9)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_10", INPUT_SECRET_RECOVERY_PHRASE_10, seed_phrase_10)
        self.enter_text("INPUT_SECRET_RECOVERY_PHRASE_11", INPUT_SECRET_RECOVERY_PHRASE_11, seed_phrase_11)

    def click_on_confirm(self):
        """
        click on confirm button
        """
        self.click("CONFIRM_BUTTON", CONFIRM_BUTTON)

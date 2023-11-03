import time

import pytest
from dcentralab_qa_infra_automation.pages.coinbasePages.CoinbaseConfirmPage import CoinbaseConfirmPage
from dcentralab_qa_infra_automation.pages.coinbasePages.CoinbaseConnectToWebsitePage import CoinbaseConnectToWebsitePage
from dcentralab_qa_infra_automation.pages.coinbasePages.CoinbaseCreatePasswordPage import CoinbaseCreatePasswordPage
from dcentralab_qa_infra_automation.pages.coinbasePages.CoinbaseCreateWalletPage import CoinbaseCreateWalletPage
from dcentralab_qa_infra_automation.pages.coinbasePages.CoinbaseImportWalletPage import CoinbaseImportWalletPage
from dcentralab_qa_infra_automation.pages.coinbasePages.CoinbasePortfolioPage import \
    CoinbasePortfolioPage
from dcentralab_qa_infra_automation.pages.coinbasePages.CoinbaseUseAnExistingWalletPage import \
    CoinbaseUseAnExistingWalletPage
from dcentralab_qa_infra_automation.utils.WalletsActionsInterface import WalletsActionsInterface

"""
Coinbase wallet actions
@Author: Efrat Cohen
@Date: 03.2023
"""


# TODO - Add messages for logger
class CoinbaseActions(WalletsActionsInterface):
    """
    coinbase actions class
    this class implements wallet actions interface.
    """

    def __init__(self, driver):
        self.driver = driver
        self.logger = pytest.logger
        self.coinbase_create_wallet_page = CoinbaseCreateWalletPage(self.driver)
        self.coinbase_use_existing_wallet_page = CoinbaseUseAnExistingWalletPage(self.driver)
        self.coinbase_import_wallet_page = CoinbaseImportWalletPage(self.driver)
        self.coinbase_create_password_page = CoinbaseCreatePasswordPage(self.driver)
        self.coinbase_portfolio_page = CoinbasePortfolioPage(self.driver)
        self.coinbase_connect_wallet_to_website_page = CoinbaseConnectToWebsitePage(self.driver)
        self.coinbase_confirm_page = CoinbaseConfirmPage(self.driver)

    def open_wallet_in_new_tab(self, url=""):
        self.driver.switch_to.new_window("tab")
        self.logger.info("tab opened")
        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])
        # Open chrome extension
        self.driver.get(url)
        self.logger.info(f"switch tab successfully with URL {url}")

    def import_wallet(self):
        """
        import coinbase wallet process implementation
        """
        # Open new tab

        self.open_wallet_in_new_tab(pytest.properties.get("coinbase.connect.url"))

        # Check if create or import wallet page loaded
        assert self.coinbase_create_wallet_page.is_page_loaded()

        # Click on already have a wallet
        self.coinbase_create_wallet_page.click_on_already_have_a_wallet()

        # Check is use an existing wallet page loaded
        assert self.coinbase_use_existing_wallet_page.is_page_loaded()

        # Click on enter recovery phrase
        self.coinbase_use_existing_wallet_page.click_on_import_wallet_seed_phrase_method()

        time.sleep(4)

        # Check if import wallet page loaded
        assert self.coinbase_import_wallet_page.is_page_loaded()

        # Insert recovery phrase
        self.coinbase_import_wallet_page.insert_recovery_phrase(
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase"))

        # Click on import wallet button
        self.coinbase_import_wallet_page.click_on_import_wallet_button()

        # Check is create password page loaded
        assert self.coinbase_create_password_page.is_page_loaded()

        # Insert password
        self.coinbase_create_password_page.insert_password(
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("coinbase_password"))

        # Verify password
        self.coinbase_create_password_page.verify_password(
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("coinbase_password"))

        # Click on agree terms checkbox
        self.coinbase_create_password_page.click_on_agree_terms_checkbox()

        # Click on submit
        self.coinbase_create_password_page.click_on_submit()

        # Check if page after wallet connection loaded
        assert self.coinbase_portfolio_page.is_page_loaded()

        time.sleep(3)

        self.close_wallet_tab()

    def connect_wallet(self):
        """
            connect to wallet implementation
        """
        w_handle = self.driver.window_handles[1]
        # Switch to pop up window
        self.driver.switch_to.window(w_handle)

        # Check is connect to website popup loaded
        assert self.coinbase_connect_wallet_to_website_page.is_page_loaded()

        # Click on connect button
        self.coinbase_connect_wallet_to_website_page.click_on_connect_button()

        time.sleep(2)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def confirm(self):
        time.sleep(5)

        # Coinbase popup instance
        w_handle = self.driver.window_handles[1]
        # Switch to pop up window
        self.driver.switch_to.window(w_handle)

        # Check is got it button exist - if exists
        if self.coinbase_confirm_page.is_got_it_button_exist():
            # Click on got_it button
            self.coinbase_confirm_page.click_on_got_it_button()

        time.sleep(1)

        # Check is confirm button exist.
        assert self.coinbase_confirm_page.is_confirm_button_exist()

        # Click on confirm button
        self.coinbase_confirm_page.click_on_confirm_button()

        time.sleep(5)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_network(self):
        pass

    def is_wallet_imported(self):
        self.open_wallet_in_new_tab(pytest.properties.get("coinbase.connect.url"))
        is_imported = False
        if self.coinbase_import_wallet_page.is_wallet_imported():
            is_imported = True

        self.close_wallet_tab()
        return is_imported

    def close_wallet_tab(self):
        time.sleep(3)
        self.driver.close()

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[0])

        time.sleep(2)

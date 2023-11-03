import time

import pytest
from dcentralab_qa_infra_automation.pages.metamaskPages.ConnectWithMetamaskPage import ConnectWithMetamaskPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskConfirmPage import MetamaskConfirmPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskCongratulationsPage import MetamaskCongratulationsPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskCreatePasswordPage import MetamaskCreatePasswordPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskImportWalletPage import MetamaskImportWalletPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskImprovePage import MetamaskImprovePage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskInstallCompletedPage import MetamaskInstallCompletedPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskSetSpendingCapPage import MetamaskSetSpendingCapPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskSwitchNetworkPage import MetamaskSwitchNetworkPage
from dcentralab_qa_infra_automation.pages.metamaskPages.WelcomeToMetamaskPage import WelcomeToMetamaskPage
from dcentralab_qa_infra_automation.utils.WalletsActionsInterface import WalletsActionsInterface

"""
MetaMask wallet actions
@Author: Efrat Cohen
@Date: 12.2022
"""


class MetamaskActions(WalletsActionsInterface):

    def __init__(self, driver):
        self.driver = driver
        self.logger = pytest.logger
        self.metamask_welcome_page = WelcomeToMetamaskPage(self.driver)
        self.metamask_improve_wallet_page = MetamaskImprovePage(self.driver)
        self.metamask_import_wallet_page = MetamaskImportWalletPage(self.driver)
        self.metamask_create_wallet_password_page = MetamaskCreatePasswordPage(self.driver)
        self.metamask_congratulations_page = MetamaskCongratulationsPage(self.driver)
        self.metamask_wallet_install_completed_page = MetamaskInstallCompletedPage(self.driver)
        self.metamask_connect_wallet_page = ConnectWithMetamaskPage(self.driver)
        self.metamask_switch_network_page = MetamaskSwitchNetworkPage(self.driver)
        self.metamask_set_spending_cap_page = MetamaskSetSpendingCapPage(self.driver)
        self.metamask_confirm_page = MetamaskConfirmPage(self.driver)

    def open_wallet_in_new_tab(self, url=""):
        """
        Open a new tab in browser
        :param url: URL to open in the new tab
        :return:
        """
        self.driver.switch_to.new_window("tab")
        self.logger.info("tab opened")
        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])
        # Open chrome extension
        self.driver.get(url)
        self.logger.info(f"switch tab successfully with URL {url}")

    def import_wallet(self):
        """
        import wallet process
        """
        # Open new tab

        self.open_wallet_in_new_tab(pytest.properties.get("metamask.connect.url"))
        self.logger.info(
            f"navigating to metamask - Import Wallet with URL: {pytest.properties.get('metamask.connect.url')}")

        # Check if metamask wallet page loaded
        assert self.metamask_welcome_page.is_page_loaded(), "Let's get started page loaded"
        # Click on agree terms
        self.metamask_welcome_page.click_on_agree_terms()
        assert self.metamask_welcome_page.is_button_exists()
        # Click on import wallet button
        self.metamask_welcome_page.click_on_import_wallet()

        # Check if improve to metamask page loaded
        assert self.metamask_improve_wallet_page.is_page_loaded(), "Help us improve MetaMask page loaded"

        # Click on I agree button
        self.metamask_improve_wallet_page.click_on_i_agree_button()
        # Check if import wallet page loaded
        assert self.metamask_import_wallet_page.is_page_loaded(), "Access your wallet with your Secret Recovery Phrase"

        # Insert secret recovery phrase
        self.metamask_import_wallet_page.insert_secret_recovery_phrase(
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_0"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_1"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_2"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_3"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_4"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_5"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_6"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_7"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_8"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_9"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_10"),
            pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_11"))

        # Click on confirm button
        self.metamask_import_wallet_page.click_on_confirm()

        assert self.metamask_create_wallet_password_page.is_page_loaded(), "Create password page loaded"

        # Insert password
        self.metamask_create_wallet_password_page.insert_password()

        # Insert confirm password
        self.metamask_create_wallet_password_page.insert_confirm_password()

        # Click on understand MetaMask checkbox
        self.metamask_create_wallet_password_page.click_on_understand_metamask_checkbox()

        # Click on import wallet
        self.metamask_create_wallet_password_page.click_on_import_wallet()

        # Check if congratulations page loaded
        assert self.metamask_congratulations_page.is_page_loaded(), "congratulations page loaded"

        # Click on got it button
        self.metamask_congratulations_page.click_on_got_it_button()

        # Check if metamask install completed page loaded
        assert self.metamask_wallet_install_completed_page.is_page_loaded(), "metamask install completed page loaded"

        # Click on next button
        self.metamask_wallet_install_completed_page.click_on_next()

        # Check is Done button exist
        assert self.metamask_wallet_install_completed_page.is_done_button_exist(), "Done button loaded"

        # Click on Done button
        self.metamask_wallet_install_completed_page.click_on_done()

        # Check is Try it out button exist
        assert self.metamask_wallet_install_completed_page.is_whats_new_popup_loaded(), "Try it out button loaded"

        # Click on Try it out button
        self.metamask_wallet_install_completed_page.close_whats_new_popup()

        self.close_wallet_tab()

    def is_wallet_imported(self):
        """
        Verify if wallet is imported by checking the URL
        :return: boolean
        """
        self.open_wallet_in_new_tab(pytest.properties.get("metamask.connect.url"))
        is_imported = False
        if "unlock" in self.driver.current_url:
            is_imported = True

        self.close_wallet_tab()
        return is_imported

    def connect_wallet(self):
        """
        connect wallet implementation
        """

        time.sleep(4)
        # Close connect with metamask extension popup
        self.metamask_connect_wallet_page.click_on_connect_with_metamask_extension_button()

        time.sleep(3)

        # Open new tab
        self.open_wallet_in_new_tab(pytest.properties.get("metamask.connect.url"))
        time.sleep(5)
        # Check if on connect with metamask page
        assert self.metamask_connect_wallet_page.is_page_loaded(), "connect with metamask page loaded"

        # Click on next button
        self.metamask_connect_wallet_page.click_on_next_button()

        # Click on connect button
        self.metamask_connect_wallet_page.click_on_connect_button()

        # Check if switch network page loaded
        assert self.metamask_switch_network_page.is_page_loaded(), "allow site to switch the network page loaded"

        # Click on switch network button
        self.metamask_switch_network_page.click_on_switch_network_button()

        self.close_wallet_tab()

    def approve_token(self):
        """
        approve token in 1st ti,e porting process
        """
        # Open new tab
        self.open_wallet_in_new_tab(pytest.properties.get("metamask.connect.url"))

        # Check if on connect with metamask page
        assert self.metamask_set_spending_cap_page.is_page_loaded(), "set spending cap page loaded"

        # Click on max button
        self.metamask_set_spending_cap_page.click_max_button()

        # Click on next button
        self.metamask_set_spending_cap_page.click_next_button()

        # Click on approve button
        self.metamask_set_spending_cap_page.click_approve_button()

        self.close_wallet_tab()

    def confirm(self):
        """
        confirm wallet process
        """
        time.sleep(5)

        self.open_wallet_in_new_tab(pytest.properties.get("metamask.connect.url"))

        # Check is confirm page loaded
        assert self.metamask_confirm_page.is_page_loaded(), "confirm page loaded"

        # Check is confirm button exist.
        assert self.metamask_confirm_page.is_confirm_button_exist()

        # Click on confirm button
        self.metamask_confirm_page.click_on_confirm_button()

        # Close MetaMask tab
        self.close_wallet_tab()

    def switch_network(self):
        pass

    def close_wallet_tab(self):
        """
        Close wallet tab and switch back to tab index 0
        :return:
        """
        time.sleep(3)
        self.driver.close()

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[0])

        time.sleep(2)

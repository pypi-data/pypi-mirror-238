import pytest

from dcentralab_qa_infra_automation.utils.HTTPMethods import get

"""
helper functions to add options to driver

@Author: Efrat Cohen
@Date: 04.2023
"""


def addExtensionToChrome():
    """
    add CRX extension to chrome
    :return: add_extension - current extension crx file
    """
    add_extension = None
    # In metamask wallet type
    if pytest.data_driven.get("wallet_type") == 'MetaMask':
        add_extension = pytest.user_dir + pytest.properties.get("metamask.extension.crx")
    elif pytest.data_driven.get("wallet_type") == 'Coinbase':
        add_extension = pytest.user_dir + pytest.properties.get("coinbase.extension.crx")
    elif pytest.data_driven.get("wallet_type") == 'Nami':
        add_extension = pytest.user_dir + pytest.properties.get("nami.extension.crx")

    return add_extension

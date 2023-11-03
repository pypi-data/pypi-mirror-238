import pytest

"""
parameters injection fixture functions - the ability to inject external param to tests via CLI

@Author: Efrat Cohen
@Date: 11.2022
"""


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--wallet", action="store", default="metamask")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    browser_value = metafunc.config.option.browser_type
    if 'browser' in metafunc.fixturenames and browser_value is not None:
        metafunc.parametrize("browser", [browser_value])
        pytest.browser_type = browser_value
    wallet_value = metafunc.config.option.wallet_type
    if 'wallet' in metafunc.fixturenames and wallet_value is not None:
        metafunc.parametrize("wallet", [wallet_value])
        pytest.wallet_type = wallet_value

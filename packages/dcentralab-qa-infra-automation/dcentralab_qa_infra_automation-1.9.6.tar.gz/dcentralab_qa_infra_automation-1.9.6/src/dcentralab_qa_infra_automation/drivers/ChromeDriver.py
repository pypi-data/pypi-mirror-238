import pytest
from dcentralab_qa_infra_automation.drivers.HelperFunctions import addExtensionToChrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

"""
init chrome driver, using ChromeDriverManager for chromeDriver installation

@Author: Efrat Cohen
@Date: 11.2022
"""


def initChromeDriver():
    """
    init chrome driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())

    if pytest.data_driven.get("headless") == "yes":
        pytest.logger.info("add headless to chrome options")
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    pytest.logger.info("start the chrome driver with options")
    driver = webdriver.Chrome(service=chrome_service, options=options)

    return driver


def initChromeDriverWithExtension():
    """
    init chrome driver with CRX extension, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.add_extension(addExtensionToChrome())
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())

    if pytest.data_driven.get("headless") == "yes":
        pytest.logger.info("add headless to chrome options")
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    pytest.logger.info("start the chrome driver with options")
    driver = webdriver.Chrome(service=chrome_service, options=options)

    return driver

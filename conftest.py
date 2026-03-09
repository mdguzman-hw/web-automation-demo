"""
Pytest configuration and shared fixtures
"""
import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from suites.CustomerPortal import CustomerPortal
from suites.Homeweb import Homeweb
from suites.QuantumAPI import QuantumAPI
from suites.SentioBetaClient import SentioBetaClient

from suites.SentioBetaClientLegacy import SentioBetaClientLegacy
from suites.SentioBetaProvider import SentioBetaProvider


@pytest.fixture(scope="session")
def driver():
    # 1: Configure Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 2: Launch Browser
    driver_instance = webdriver.Chrome(options=chrome_options)

    # 3. YIELD - give driver to the tests
    yield driver_instance

    # 4: Close Browser
    driver_instance.quit()


load_dotenv()


@pytest.fixture(scope="session")
def credentials():
    return {
        "personal": {
            "email": os.getenv("PERSONAL_EMAIL"),
            "password": os.getenv("PERSONAL_PASSWORD")
        },
        "dsg_demo": {
            "email": os.getenv("DSG_DEMO_EMAIL"),
            "password": os.getenv("DSG_DEMO_PASSWORD")
        },
        "sentio": {
            "email": os.getenv("SENTIO_EMAIL"),
            "password": os.getenv("SENTIO_PASSWORD")
        },
        "hhi_demo": {
            "email": os.getenv("HHI_DEMO_EMAIL"),
            "password": os.getenv("HHI_DEMO_PASSWORD")
        }
    }


@pytest.fixture(scope="session")
def language():
    return os.getenv("LANGUAGE", "en")


@pytest.fixture(scope="session")
def homeweb(driver, language):
    homeweb = Homeweb(driver, language)
    return homeweb


@pytest.fixture(scope="session")
def quantum(driver, language):
    quantum = QuantumAPI(driver, language)
    return quantum


@pytest.fixture(scope="session")
def customer_portal(driver, language):
    portal = CustomerPortal(driver, language)
    return portal


@pytest.fixture(scope="session")
def sentio_beta_client(driver, language):
    sentio_client = SentioBetaClient(driver, language)
    return sentio_client

@pytest.fixture(scope="session")
def sentio_beta_client_legacy(driver, language):
    sentio_client = SentioBetaClientLegacy(driver, language)
    return sentio_client

@pytest.fixture(scope="session")
def sentio_beta_provider(driver, language):
    sentio_provider = SentioBetaProvider(driver, language)
    return sentio_provider

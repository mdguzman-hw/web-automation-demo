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
from suites.HomewebBeta import HomewebBeta
from suites.QuantumAPI import QuantumAPI
from suites.QuantumAPIBeta import QuantumAPIBeta
from suites.SentioBetaClient import SentioBetaClient
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


# @pytest.fixture(scope="session")
# def homeweb(driver, language):
#     homeweb = Homeweb(driver, language)
#     return homeweb

# @pytest.fixture(scope="session")
# def homeweb_beta(driver, language):
#     homeweb_beta = HomewebBeta(driver, language)
#     return homeweb_beta

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help="Environment: prod | beta | all"
    )


def pytest_collection_modifyitems(items):
    def get_group(item):
        name = item.name

        import re
        match = re.search(r"test_bat_web_(\d+)", name)
        order = int(match.group(1)) if match else 999

        # 🔥 ENV FIRST (this is the fix)
        if "[PROD]" in name:
            env = 0
        elif "[BETA]" in name:
            env = 1
        elif "_beta" in name.lower():
            env = 1
        else:
            env = 2

        return (env, order)

    items.sort(key=get_group)


@pytest.fixture(params=["prod", "beta"], ids=["PROD", "BETA"], scope="session")
def homeweb(request, driver, language):
    env_flag = request.config.getoption("--env")

    # allow filtering
    if env_flag != "all" and request.param != env_flag:
        pytest.skip(f"Skipping {request.param} environment")

    if request.param == "prod":
        instance = Homeweb(driver, language)
    else:
        instance = HomewebBeta(driver, language)

    instance.env = request.param
    return instance


@pytest.fixture(scope="session")
def quantum(driver, language):
    quantum = QuantumAPI(driver, language)
    return quantum


@pytest.fixture(scope="session")
def quantum_api_beta(driver, language):
    quantum_api_beta = QuantumAPIBeta(driver, language)
    return quantum_api_beta


@pytest.fixture(scope="session")
def customer_portal(driver, language):
    portal = CustomerPortal(driver, language)
    return portal


@pytest.fixture(scope="session")
def sentio_beta_client(driver, language):
    sentio_client = SentioBetaClient(driver, language)
    return sentio_client


@pytest.fixture(scope="session")
def sentio_beta_provider(driver, language):
    sentio_provider = SentioBetaProvider(driver, language)
    return sentio_provider

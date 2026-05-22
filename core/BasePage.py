# Copyright © 2026 - Homewood Health Inc.

import os
import time
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, language):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.language = language

    def click_element(self, by, locator):
        for attempt in range(3):
            try:
                element = self.wait.until(
                    expected_conditions.presence_of_element_located((by, locator))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )
                time.sleep(0.5)
                self.wait.until(
                    expected_conditions.element_to_be_clickable((by, locator))
                ).click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if attempt == 2:
                    raise
                time.sleep(0.3)

    def take_screenshot(self, name, logger=None):
        from conftest import _run_timestamp, _reports_dir
        os.makedirs(_reports_dir, exist_ok=True)
        env = getattr(self, "env", "")
        env_suffix = f"_{env.upper()}" if env else ""
        filename = f"{_run_timestamp}_{name}{env_suffix}.png"
        self.driver.save_screenshot(f"{_reports_dir}/{filename}")
        if logger:
            logger(f"Screenshot saved: {filename}")

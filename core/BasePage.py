# Copyright © 2026 - Homewood Health Inc.

import os
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, language):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.language = language

    def click_element(self, by, locator):
        # 1: Find element
        element = self.wait.until(
            expected_conditions.presence_of_element_located((by, locator))
        )

        # 2: Scroll element into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

        # 3: Wait for layout to stabilize; re-fetch on stale reference
        def is_stable(d):
            nonlocal element
            try:
                return element.is_displayed() and element.is_enabled()
            except StaleElementReferenceException:
                element = d.find_element(by, locator)
                return False

        self.wait.until(is_stable)

        # 4: Small pause to allow any final reflows
        time.sleep(0.5)
        clickable_element = self.wait.until(
            expected_conditions.element_to_be_clickable((by, locator))
        )

        # 5: Click element
        clickable_element.click()

    def take_screenshot(self, name, logger=None):
        from conftest import _run_timestamp, _reports_dir
        os.makedirs(_reports_dir, exist_ok=True)
        env = getattr(self, "env", "")
        env_suffix = f"_{env.upper()}" if env else ""
        filename = f"{_run_timestamp}_{name}{env_suffix}.png"
        self.driver.save_screenshot(f"{_reports_dir}/{filename}")
        if logger:
            logger(f"Screenshot saved: {filename}")

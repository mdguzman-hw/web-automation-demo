from core.BasePage import BasePage
from core.Constants import CUSTOMER_PORTAL_BASE_URL, CUSTOMER_PORTAL_DOMAIN
from core.Header import Header
from selenium.webdriver.support import expected_conditions


class CustomerPortal(BasePage):
    @property
    def current_url(self):
        return self.driver.current_url

    def __init__(self, driver, language, env, quantum):
        super().__init__(driver, language)

        if env == "prod":
            self.base_url = CUSTOMER_PORTAL_BASE_URL
            self.domain = CUSTOMER_PORTAL_DOMAIN
        else:
            self.base_url = CUSTOMER_PORTAL_BASE_URL
            self.domain = CUSTOMER_PORTAL_DOMAIN

        self.quantum = quantum
        self._is_authenticated = False
        self.header = None
        self.update_header()
        self.user_type = ""

    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="customer_portal", language=self.language, user=user_type)

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()

    def is_authenticated(self):
        return self._is_authenticated

    def wait_for_portal_login(self):
        return self.wait.until(
            lambda d: "portal.homewoodhealth" in d.current_url.lower() and "/app/en" in d.current_url.lower()
        )

    def wait_for_power_bi_report(self):
        # 1: Locate embed container
        self.wait.until(
            expected_conditions.presence_of_element_located(("id", "embedContainer"))
        )

        # 2: Locate and switch to iframe content
        iframe = self.wait.until(
            expected_conditions.presence_of_element_located(("tag name", "iframe"))
        )
        self.driver.switch_to.frame(iframe)

        # 3: Wait for visual-style element to load
        self.wait.until(
            expected_conditions.presence_of_element_located(("css selector", "[data-testid=\"visual-style\"]"))
        )

        # 4: Ensure the visual actually rendered content (svg or visual-content-desc)
        self.wait.until(
            expected_conditions.presence_of_element_located((
                "css selector",
                "[data-testid=\"visual-style\"] svg, [data-testid=\"visual-style\"] [data-testid=\"visual-content-desc\"]",
            ))
        )

        # 6: Switch back to main content
        self.driver.switch_to.default_content()
        return True

    def wait_for_tableau_report(self):
        # 1: Locate embed container
        self.wait.until(
            expected_conditions.presence_of_element_located(("id", "embedContainer"))
        )

        # 2: Locate and switch to iframe content
        iframe = self.wait.until(
            expected_conditions.presence_of_element_located(("tag name", "iframe"))
        )
        self.driver.switch_to.frame(iframe)

        # 3: Wait for tab zone elements to load
        self.wait.until(
            expected_conditions.presence_of_element_located(("css selector", ".tab-zone"))
        )

        # 4: Wait for tab loaders to complete
        self.wait.until(
            expected_conditions.invisibility_of_element_located(("css selector", ".tab-loader"))
        )

        # 6: Switch back to main content
        self.driver.switch_to.default_content()
        return True

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from core.BasePage import BasePage
from core.Constants import SENTIO_BETA_PROVIDER_BASE_URL, SENTIO_BETA_PROVIDER_DOMAIN
from core.Header import Header


class SentioProvider(BasePage):
    # Properties
    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def classic_dashboard_endpoint(self):
        return "/app/" + self.language + "/sentio/v2/patients"

    @property
    def new_dashboard_endpoint(self):
        return "/app/" + self.language + "/sentio/v3/patients"

    def __init__(self, driver, language, env, quantum):
        super().__init__(driver, language)

        if env == "prod":
            self.base_url = SENTIO_BETA_PROVIDER_BASE_URL
            self.domain = SENTIO_BETA_PROVIDER_DOMAIN
        else:
            self.base_url = SENTIO_BETA_PROVIDER_BASE_URL
            self.domain = SENTIO_BETA_PROVIDER_DOMAIN

        self.quantum = quantum
        self._is_authenticated = False
        self.header = None
        self.update_header()

    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="sentio_beta_provider", language=self.language, user=user_type)

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()

    def wait_for_login(self):
        self.set_authenticated(True)

        self.wait.until(
            lambda d: self.domain in self.current_url.lower()
        )

        return self.wait.until(
            expected_conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".loading-container.loadingPage")
            )
        )

    def wait_for_dashboard(self, dashboard_type):

        if dashboard_type == "classic":
            self.wait.until(
                lambda d: self.classic_dashboard_endpoint in d.current_url.lower()
            )
        elif dashboard_type == "new":
            self.wait.until(
                lambda d: self.new_dashboard_endpoint in d.current_url.lower()
            )

        self.wait.until(
            expected_conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".loading-container.loadingPage")
            )
        )

        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "managerPatient"))
        )

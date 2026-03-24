from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from core.BasePage import BasePage
from core.Constants import QUANTUM_API_BASE_URL, QUANTUM_API_DOMAIN, QUANTUM_API_BETA_BASE_URL, QUANTUM_API_BETA_DOMAIN
from core.Header import Header
from core.Login import LoginPage


class QuantumAPI(BasePage):
    @property
    def current_url(self):
        return self.driver.current_url


    def __init__(self, driver, language, env):
        super().__init__(driver, language)

        if env == "prod":
            self.base_url = QUANTUM_API_BASE_URL
            self.domain = QUANTUM_API_DOMAIN
        else:
            self.base_url = QUANTUM_API_BETA_BASE_URL
            self.domain = QUANTUM_API_BETA_DOMAIN

        self.landing_url = self.base_url + "/" + language
        self.elements = LoginPage.EN if language == "en" else LoginPage.FR
        self._is_authenticated = False
        self.header = None
        self.update_header()

    def login(self, email, password):
        inputs = self.elements["elements"]["inputs"]

        # Email step
        self.input(inputs["email_address"], email)
        self.submit()

        password_input = self.wait_for_password()
        assert password_input.is_displayed()

        # Password step
        self.input(inputs["password"], password)
        self.submit()

    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="quantum_api", language=self.language, user=user_type)

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()

    def is_authenticated(self):
        return self._is_authenticated

    def input(self, input_identifier, input_value):
        email_input = self.wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, input_identifier))
        )
        email_input.clear()
        email_input.send_keys(input_value)

    def submit(self):
        self.click_element(By.XPATH, self.elements["elements"]["buttons"]["next"])

    def wait_for_password(self):
        xpath = self.elements["elements"]["inputs"]["password"]
        return self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))

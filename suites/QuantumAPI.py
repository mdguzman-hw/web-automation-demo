# Copyright © 2026 - Homewood Health Inc.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from core.BasePage import BasePage
from core.Constants import QUANTUM_API_BASE_URL, QUANTUM_API_DOMAIN, QUANTUM_API_BETA_BASE_URL, QUANTUM_API_BETA_DOMAIN, QUANTUM_API_STAGING_BASE_URL, QUANTUM_API_STAGING_DOMAIN
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
        elif env == "staging":
            self.base_url = QUANTUM_API_STAGING_BASE_URL
            self.domain = QUANTUM_API_STAGING_DOMAIN
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

    def wait_for_url_path(self, path):
        return self.wait.until(
            expected_conditions.url_contains(path)
        )

    def navigate_registration(self, program_id):
        self.driver.get(f"{self.base_url}/{self.language}/register/{program_id}")

    def wait_for_org_search(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "orgSearch"))
        )

    def search_org(self, query):
        field = self.wait.until(
            expected_conditions.element_to_be_clickable((By.ID, "orgSearch"))
        )
        field.clear()
        field.send_keys(query)

    def wait_for_org_results(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#orgResults .list[role='listbox']")
            )
        )

    def select_org(self, org_name):
        self.click_element(
            By.XPATH,
            f"//a[@role='option']//span[@class='name' and normalize-space()='{org_name}']/.."
        )

    def wait_for_role_selection(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.reg-roles[role='radiogroup']")
            )
        )

    def select_role(self, role):
        locator = (By.XPATH, f"//input[@data-role='{role}']/parent::label")
        self.wait.until(expected_conditions.element_to_be_clickable(locator)).click()

    def continue_registration(self):
        self.click_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")

    def continue_from_verify(self):
        self.click_element(By.XPATH, "//button[contains(normalize-space(), 'Continue')]")

    def wait_for_registration_details(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "firstName"))
        )

    def fill_password_form(self, password, marketing_opt_in=False):
        for field_id, value in [("password", password), ("confirmPassword", password)]:
            field = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, field_id)))
            field.clear()
            field.send_keys(value)

        toggle = self.driver.find_element(By.CSS_SELECTOR, "input[name='marketingOptIn']")
        if toggle.is_selected() != marketing_opt_in:
            self.click_element(By.CSS_SELECTOR, "label.reg-toggle span.track")

        self.click_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")

    def enter_email_verification_code(self, code):
        for i, digit in enumerate(code):
            field = self.wait.until(
                expected_conditions.element_to_be_clickable((By.ID, f"emailCodeDigit{i}"))
            )
            field.clear()
            field.send_keys(digit)
        self.click_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")

    def fill_registration_details(self, first_name, last_name, preferred_name, email, dob):
        for field_id, value in [("firstName", first_name), ("lastName", last_name), ("preferredName", preferred_name), ("email", email)]:
            field = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, field_id)))
            field.clear()
            field.send_keys(value)

        dob_field = self.driver.find_element(By.ID, "dob")
        self.driver.execute_script("arguments[0].value = arguments[1];", dob_field, dob)

        self.click_element(By.CSS_SELECTOR, "label.reg-toggle span.track")

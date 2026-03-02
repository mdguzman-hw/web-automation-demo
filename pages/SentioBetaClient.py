import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select

from pages.BasePage import BasePage
from pages.Constants import SENTIO_BETA_CLIENT_BASE_URL, SENTIO_BETA_CLIENT_DOMAIN
from pages.Header import Header


class SentioBetaClient(BasePage):
    # Properties
    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def base_url(self):
        return SENTIO_BETA_CLIENT_BASE_URL

    @property
    def landing_url(self):
        return self.base_url + "/" + self.language

    @property
    def domain(self):
        return SENTIO_BETA_CLIENT_DOMAIN

    @property
    def dashboard_endpoint(self):
        return "/app/" + self.language + "/dashboard"

    @property
    def landing_elements(self):
        return SentioLanding.EN["elements"] if self.language == "en" else SentioLanding.FR["elements"]

    @property
    def program_status_endpoint(self):
        return "/status" in self.current_url

    @property
    def module_complete_endpoint(self):
        return "/complete" in self.current_url

    def __init__(self, driver, language):
        super().__init__(driver, language)
        self._is_authenticated = False
        self._is_landing = False
        self.programs = Programs.EN if self.language == "en" else Programs.FR
        self.header = None
        self.current_goal = None
        self.update_header()

    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="sentio_beta_client", language=self.language, user=user_type)

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()

    def navigate_landing(self):
        self.driver.get(self.landing_url)
        self._is_landing = True

    def go_back(self):
        self.driver.back()
        self.wait.until(
            lambda d: self.domain in d.current_url
        )
        self.driver.execute_script("window.scrollBy(0, 0);")

    def wait_for_dashboard(self):
        self._is_landing = False

        self.set_authenticated(True)

        return self.wait.until(
            lambda d: self.dashboard_endpoint in d.current_url.lower()
        )

    # TODO: Update this to click on the Header-Logo or Header-Dashboard instead of just URL injection and navigation
    def navigate_dashboard(self):
        self.driver.get(self.base_url + self.dashboard_endpoint)
        self.in_progress_programs()

    def navigate_overview(self, title):
        # 1: Find program card by title
        program_card = self.wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, f"//div[contains(@class,'card-container')]//p[@class='h4' and normalize-space(text())='{title}']/ancestor::div[contains(@class,'card-container')]"))
        )

        # 2. Scroll the program card into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", program_card
        )
        self.wait.until(lambda d: program_card.is_displayed() and program_card.is_enabled())
        time.sleep(0.5)

        # 3: Find button within program card
        button = program_card.find_element(By.CSS_SELECTOR, "a.btn.btn-primary")
        self.wait.until(lambda d: button.is_displayed() and button.is_enabled())

        # 4: Click button
        button.click()

    def navigate_assessment(self):
        button = self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary"))
        )

        button.click()

    def complete_assessment(self):
        while "/results" not in self.current_url:
            # 1. Get currently visible question
            current_question = self.wait.until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "div.item-question-assessment:not([style*='display: none'])"))
            )

            # 2. Pick a random answer
            buttons = current_question.find_elements(By.CSS_SELECTOR, "button.btn-answer")
            choice = random.choice(buttons)

            # 3. Scroll into view & click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", choice)
            self.wait.until(lambda d: choice.is_displayed() and choice.is_enabled())
            choice.click()

            # 4. Wait until next question appears or results page
            self.wait.until(
                lambda d: "/results" in d.current_url or
                          d.find_element(By.CSS_SELECTOR, "div.item-question-assessment:not([style*='display: none'])") != current_question
            )

    def start_program(self, tier, province):
        # 1: Ensure form is visible
        self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "startProgramForm"))
        )

        # 2: Select Tier (radio by value)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tier)
        self.wait.until(lambda d: tier.is_displayed() and tier.is_enabled())
        time.sleep(0.5)
        tier.click()

        # 3: Select Province
        province_select = Select(self.wait.until(
            expected_conditions.presence_of_element_located((By.ID, "jurisdictionSelect"))
        ))
        province_select.select_by_value(province)

        # 4: Wait for Start button to become enabled
        submit_btn = self.wait.until(
            expected_conditions.element_to_be_clickable((By.ID, "submitBtn"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        self.wait.until(lambda d: submit_btn.is_displayed() and submit_btn.is_enabled())
        time.sleep(0.5)

        # 5: Click Start
        submit_btn.click()

    def continue_program(self, title):
        # 1: Find program tile by title
        program_tile = self.wait.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class,'item-dashboard-active')]//h2[normalize-space(text())='{title}']/ancestor::div[contains(@class,'item-dashboard-active')]")
            )
        )

        # 2: Scroll program tile into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", program_tile)
        self.wait.until(lambda d: program_tile.is_displayed() and program_tile.is_enabled())
        time.sleep(0.5)

        # 3: Find table of contents button within tile
        toc_button = program_tile.find_element(By.CSS_SELECTOR, "a.btn-outline-muted")
        self.wait.until(lambda d: toc_button.is_displayed() and toc_button.is_enabled())

        # 4: Click button
        toc_button.click()

    def available_programs(self):
        program_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.card-container")
        programs = []

        for program in program_cards:
            title = program.find_element(By.CSS_SELECTOR, "p.h4").text
            href = program.find_element(By.CSS_SELECTOR, "a.btn.btn-primary").get_attribute("href")
            status_elements = program.find_elements(By.CSS_SELECTOR, ".overlay-content")
            status = status_elements[0].text.strip() if status_elements else None
            programs.append(ProgramCard(title, href, status))

        return programs

    def in_progress_programs(self):
        program_tiles = self.driver.find_elements(By.CSS_SELECTOR, ".item.item-dashboard.item-dashboard-active")
        in_progress_programs = []

        for program in program_tiles:
            title = program.find_element(By.CSS_SELECTOR, "h2.header").text
            href_toc = program.find_element(By.CSS_SELECTOR, "a.btn.btn-outline-muted").get_attribute("href")
            href_next_activity = program.find_element(By.CSS_SELECTOR, "a.btn.btn-primary").get_attribute("href")
            href_withdraw = program.find_element(By.CSS_SELECTOR, "p.end-service-note a").get_attribute("href")
            in_progress_programs.append(ProgramTile(title, href_toc, href_next_activity, href_withdraw))

        return in_progress_programs

    def available_tiers(self):
        # TIER_1
        # TIER_2
        # TIER_3

        tier_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.item-tier")
        tiers = {}

        for tier in tier_elements:
            input_elem = tier.find_element(By.CSS_SELECTOR, "input.btn-check")
            key = input_elem.get_attribute("value")
            clickable_element = tier.find_element(By.CSS_SELECTOR, "label.btn")

            tiers[key] = clickable_element

        return tiers

    def available_provinces(self):
        # Alberta
        # British Columbia
        # Manitoba
        # New Brunswick
        # Newfoundland and Labrador
        # Nova Scotia
        # Ontario
        # Prince Edward Island
        # Québec
        # Saskatchewan
        # Yukon Territory
        # Northwest Territories
        # Nunavut

        select_element = Select(self.driver.find_element(By.ID, "jurisdictionSelect"))

        provinces = {}

        for option in select_element.options:
            key = option.get_attribute("key")
            value = option.get_attribute("value")

            # Skip placeholder
            if not key:
                continue

            provinces[key] = value

        return provinces

    def available_modules(self):
        modules = self.driver.find_elements(
            By.CSS_SELECTOR, "#previewAccordion .accordion-item"
        )

        return [ModuleTile(module) for module in modules]

    def wait_for_activity_content(self):
        element = self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "page-program-flow"))
        )

        if "exercises/start" in self.driver.current_url:
            self.setup_exercise()

        return element

    def start_goal(self):
        # 1: Find continue button
        button = self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "btn-primary"))
        )

        # 2. Scroll the button into view, if required
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        self.wait.until(lambda d: button.is_displayed() and button.is_enabled())

        # 3: Click button
        button.click()

        assert self.wait_for_activity_content()

        self.next_activity()
        assert self.wait_for_activity_content()

    def next_activity(self):
        # 1: Find the next button container
        next_button_container = self.wait.until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".container-program-progress-footer .item-program-progress.next")
            )
        )

        # 2: Scroll to the next button container
        self.driver.execute_script(
            # ALTERNATIVE, however, jumps to the element rather than scroll
            # "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
            "arguments[0].scrollIntoView({block: 'center'});",
            next_button_container
        )
        time.sleep(1)

        # 3: Wait for next button to be clickable
        next_button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, ".container-program-progress-footer .item-program-progress.next a")
            )
        )

        # 4: Click next button
        next_button.click()

    def continue_goal(self):
        module_accordions = self.driver.find_elements(By.CSS_SELECTOR, "div.accordion-header")

        for module in module_accordions:
            if module.find_elements(By.CSS_SELECTOR, ".badge-in-progress"):
                self.current_goal = module.find_element(By.CSS_SELECTOR, "div.button-header span.title.font-size-lg").text
                continue_btn = module.find_element(
                    By.CSS_SELECTOR,
                    "a.btn.btn-primary-light.font-size-sm"
                )
                continue_btn.click()
                break

        self.wait_for_activity_content()

    def complete_goal(self):
        while not self.module_complete_endpoint:
            old_url = self.driver.current_url

            self.next_activity()
            assert self.wait_for_activity_content()

            if self.driver.current_url.endswith("/input"):
                return

            # Wait for the URL to change
            self.wait.until(expected_conditions.url_changes(old_url))

        self.complete_goal_survey()
        assert self.wait_for_activity_content()

        toc = "Table of contents" if self.language == "en" else "Table des matières"
        # toc_link = progress_container.find_element(By.LINK_TEXT, toc)
        toc_link = self.wait.until(expected_conditions.presence_of_element_located(
            (By.LINK_TEXT, toc)
        ))

        toc_link.click()

        assert self.program_status_endpoint
        assert self.current_goal_completed()
        self.current_goal = None

    def current_goal_completed(self):
        module = self.driver.find_element(
            By.XPATH,
            f"//div[@class='accordion-header']//span[@class='title font-size-lg' and text()='{self.current_goal}']/ancestor::div[@class='button-header']"
        )
        badge = module.find_element(By.CSS_SELECTOR, "span.badge")
        return self.wait.until(lambda driver: "badge-complete" in badge.get_attribute("class"))

    def complete_goal_survey(self):
        # 1: Find the form container
        self.wait.until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, "form.form-completed-survey")
        ))

        # 2: Find questions in the form
        questions = self.wait.until(expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "form.form-completed-survey div.row")
        ))

        for question in questions:
            # 3: Find all radio buttons inside this row
            options = question.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            # 4: Pick a random option
            choice = random.choice(options)
            # Wait for the radio button to be clickable
            label = question.find_element(By.CSS_SELECTOR, f"label[for='{choice.get_attribute('id')}']")
            # self.wait.until(expected_conditions.element_to_be_clickable(choice))
            label.click()

        submit_button = self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "form.form-completed-survey button[type='submit']"))
        )

        submit_button.click()

    def withdraw_program(self, program):
        # 1: Locate program tile
        program_tile = self.driver.find_element(
            By.XPATH,
            f'//h2[normalize-space()="{program.title}"]/ancestor::div[contains(@class,"item-dashboard")]'
        )

        # 2: Find withdraw link within the specified program
        withdraw_link = program_tile.find_element(
            By.CSS_SELECTOR, 'a[href*="withdraw"]'
        )

        # 3: Scroll to withdraw link, if required
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            withdraw_link
        )
        time.sleep(0.5)

        # 4: Click link
        withdraw_link.click()

        assert program.href_withdraw in self.current_url.lower()

        self.end_program_survey()

    def end_program_survey(self):
        # 1: Find the form container
        self.wait.until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, "form.form-goal-survey")
        ))

        # 2: Find questions in the form
        questions = self.wait.until(expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "form.form-goal-survey div.row")
        ))

        for question in questions:
            # 3: Find all radio buttons inside this row
            options = question.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            # 4: Pick a random option
            choice = random.choice(options)
            # Wait for the radio button to be clickable
            label = question.find_element(By.CSS_SELECTOR, f"label[for='{choice.get_attribute('id')}']")
            # self.wait.until(expected_conditions.element_to_be_clickable(choice))
            label.click()

        submit_button = self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "form.form-goal-survey button[type='submit']"))
        )

        submit_button.click()

    def setup_exercise(self):
        text = "Setup Tasks" if self.language == "en" else "Tâches de configuration"

        setup_button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, f'//button[@type="submit" and normalize-space()="{text}"]')
            )
        )

        setup_button.click()

        assert "/exercises/" in self.driver.current_url
        assert self.driver.current_url.endswith("/start")

        self.start_exercise()

    def start_exercise(self):
        # Wait for the start task button
        start_button = self.wait.until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a.btn.btn-primary[href*="/exercises/"][href$="/input"]')
            )
        )

        # Scroll into view (prevents click interception)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            start_button
        )

        start_button.click()

        # Wait for navigation to input page
        assert "/exercises/" in self.driver.current_url
        assert self.driver.current_url.endswith("/input")


class SentioLanding:
    EN = {
        "elements": {
            "get_started": "Get Started",
            "login": "Login"
        }
    }

    FR = {
        "elements": {
            "get_started": "Commencer",
            "login": "Ouvrir une session"
        }
    }


class Programs:
    EN = {
        "anxiety": "Anxiety",
        "anxiety_depression": "Co-Existing Anxiety and Depression",
        "depression": "Depression",
        "mental_health": "Mental Health and Wellness",
    }

    FR = {
        "anxiety": "Anxiété",
        "anxiety_depression": "Anxiété et dépression coexistantes",
        "depression": "Dépression",
        "mental_health": "Santé mentale et bien-être",
    }


class ProgramCard:
    def __init__(self, title, href, status):
        self.title = title
        self.href = href
        self.status = status


class ProgramTile:
    def __init__(self, title, href_toc, href_next_activity, href_withdraw):
        self.title = title
        self.href_toc = href_toc
        self.href_next_activity = href_next_activity
        self.href_withdraw = href_withdraw


class ProgramTier:
    def __init__(self, clickable_element):
        self.element = clickable_element

    def select(self):
        self.element.click()


class ModuleTile:
    def __init__(self, root_element):
        self._root = root_element

    @property
    def title(self):
        return self._root.find_element(By.CSS_SELECTOR, ".title").text

    @property
    def status(self):
        badges = self._root.find_elements(By.CSS_SELECTOR, ".badge-container .badge")
        return badges[0].text.strip() if badges else "N/A"

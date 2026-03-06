import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select

from core.BasePage import BasePage
from core.Constants import SENTIO_BETA_CLIENT_BASE_URL, SENTIO_BETA_CLIENT_DOMAIN
from core.Header import Header


class SentioBetaClientTest(BasePage):
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

    @property
    def program_survey_endpoint(self):
        return "/survey" in self.current_url

    def __init__(self, driver, language):
        super().__init__(driver, language)
        self._is_authenticated = False
        self._is_landing = False
        self.programs = Programs.EN if self.language == "en" else Programs.FR
        self.header = None
        self.current_module = None
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

    def navigate_dashboard(self):
        self.click_element(By.CSS_SELECTOR, self.header.elements["buttons"]["dashboard"])
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
        self.click_element(By.CSS_SELECTOR, "a.btn.btn-primary")

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
            title = program.find_element(By.CSS_SELECTOR, "p.h4").text.strip()
            href = program.find_element(By.CSS_SELECTOR, "a.btn.btn-primary").get_attribute("href")
            status_elements = program.find_elements(By.CSS_SELECTOR, ".overlay-content")
            status = status_elements[0].text.strip() if status_elements else None
            programs.append(ProgramCard(title, href, status))

        return programs

    def in_progress_programs(self):
        program_tiles = self.driver.find_elements(By.CSS_SELECTOR, ".item.item-dashboard.item-dashboard-active")
        in_progress_programs = []

        for program in program_tiles:
            title = program.find_element(By.CSS_SELECTOR, "h2.header").text.strip()
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
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "page-program-flow"))
        )

    def start_goal(self):
        # # 1: Find continue button
        # button = self.wait.until(
        #     expected_conditions.visibility_of_element_located((By.CLASS_NAME, "btn-primary"))
        # )
        #
        # # 2. Scroll the button into view, if required
        # self.driver.execute_script(
        #     "arguments[0].scrollIntoView({block: 'center'});", button
        # )
        # self.wait.until(lambda d: button.is_displayed() and button.is_enabled())
        # button.click()

        # 3: Click button
        self.click_element(By.CLASS_NAME, "btn-primary")
        assert self.wait_for_activity_content()

        # 4: First activity page is just the overview, navigate to start goal
        self.next_activity()
        assert self.wait_for_activity_content()
        self.current_module = self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".item-program-progress.current .item-inner .item-title"))
        ).text.strip()

        # 5: Navigate back to status page by clicking table of contents link
        self.navigate_toc()

    def navigate_toc(self):
        toc = "Table of contents" if self.language == "en" else "Table des matières"
        self.wait.until(expected_conditions.presence_of_element_located((By.LINK_TEXT, toc)))
        time.sleep(1)
        self.click_element(By.LINK_TEXT, toc)
        assert self.program_status_endpoint

    def continue_goal(self):
        self.wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.accordion-header")))
        module_accordions = self.driver.find_elements(By.CSS_SELECTOR, "div.accordion-header")
        for module in module_accordions:
            if module.find_elements(By.CSS_SELECTOR, ".badge-in-progress"):
                self.current_module = module.find_element(By.CSS_SELECTOR, "div.button-header span.title.font-size-lg").text.strip()
                continue_btn = module.find_element(By.CSS_SELECTOR, "a.btn.btn-primary-light.font-size-sm")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
                self.wait.until(lambda d: continue_btn.is_displayed() and continue_btn.is_enabled())
                time.sleep(1)
                continue_btn.click()
                break

        assert self.wait_for_activity_content()

    def complete_goal(self):
        while not self.module_complete_endpoint:
            old_url = self.current_url

            self.next_activity()
            assert self.wait_for_activity_content()

            if self.is_exercise():
                self.complete_exercise()
                continue

            if self.has_media():
                self.play_media()

            self.wait.until(expected_conditions.url_changes(old_url))


        self.complete_goal_survey()

        if self.program_survey_endpoint:
            self.complete_program_survey()
            return

        self.navigate_toc()
        assert self.program_status_endpoint

    def complete_program_survey(self):
        # Click "Finish program" button
        finish_btn = self.wait.until(expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.btn-outline-muted")
        ))
        finish_btn.click()

        # Hidden form is now revealed — submit it
        self.wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, ".toggle-target")
        ))
        self.click_element(By.CSS_SELECTOR, ".toggle-target button[type='submit']")

    def is_exercise(self):
        next_btn = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".container-program-progress-footer .item-program-progress.next .item-inner"
        )
        if not next_btn:
            return False
        classes = next_btn[0].get_attribute("class")
        return "locked" in classes or bool(next_btn[0].find_elements(By.CSS_SELECTOR, ".overlay"))

    def complete_exercise(self):
        if "exercises/start" in self.current_url:
            # Type A - multi-task: setup then loop tasks until next unlocks
            self.setup_exercise()
            while True:
                self.start_exercise()
                self.complete_steps()
                # Wait to be back on task list
                self.wait.until(expected_conditions.url_contains("/start"))

                # If another unlocked task exists, continue loop
                next_task = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'a.btn.btn-primary[href*="/exercises/"][href$="/input"]'
                )
                if next_task:
                    continue

                # No more tasks - check if footer next is unlocked
                next_btn = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".container-program-progress-footer .item-program-progress.next .item-inner"
                )
                if next_btn and "locked" not in next_btn[0].get_attribute("class"):
                    break
        else:
            # Type B - embedded single-task: complete steps, submit navigates automatically
            self.complete_steps()

    def setup_exercise(self):
        # text = "Setup Tasks" if self.language == "en" else "Tâches de configuration"
        # self.wait.until(
        #     expected_conditions.element_to_be_clickable(
        #         (By.XPATH, f'//button[@type="submit" and normalize-space()="{text}"]')
        #     )
        # ).click()
        self.click_element(By.CSS_SELECTOR, "button[type='submit']")
        self.wait.until(expected_conditions.url_contains("/exercises/"))
        self.wait.until(expected_conditions.url_contains("/start"))

    def start_exercise(self):
        # start_button = self.wait.until(
        #     expected_conditions.element_to_be_clickable(
        #         (By.CSS_SELECTOR, 'a.btn.btn-primary[href*="/exercises/"][href$="/input"]')
        #     )
        # )
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_button)
        # time.sleep(0.5)
        # start_button.click()
        self.click_element(By.CSS_SELECTOR, 'a.btn.btn-primary[href*="/exercises/"][href$="/input"]')
        self.wait.until(expected_conditions.url_contains("/input"))

    def select_previous_entry(self):
        previous_entry_btn = self.driver.find_elements(By.CSS_SELECTOR, "button[data-bs-target='#modal-form-previous-entry']")
        if not previous_entry_btn:
            return False

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", previous_entry_btn[0])
        self.wait.until(lambda d: previous_entry_btn[0].is_displayed() and previous_entry_btn[0].is_enabled())
        time.sleep(1)
        previous_entry_btn[0].click()
        time.sleep(1)
        self.wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".modal.show")))

        select_entry_btns = self.wait.until(expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".modal.show .item-exercise-entry .btn-outline-muted")
        ))
        # select_entry_btns = self.driver.find_elements(By.CSS_SELECTOR, ".modal.show .item-exercise-entry .btn-outline-muted")
        selected_entry = random.choice(select_entry_btns)

        # DEBUGGING ONLY
        # entry_item = selected_entry.find_element(By.XPATH, "./ancestor::div[contains(@class,'item-exercise-entry')]")
        # pre_title = entry_item.find_element(By.CSS_SELECTOR, ".pre-title").text.strip()
        # title = entry_item.find_element(By.CSS_SELECTOR, ".title").text.strip()
        # print(f"SELECTED ENTRY: {pre_title} | {title}. Press enter to continue")

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected_entry)
        self.wait.until(lambda d: selected_entry.is_displayed() and selected_entry.is_enabled())
        time.sleep(1)
        selected_entry.click()
        self.wait.until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, ".modal.show")))
        time.sleep(1)
        return True

    def complete_steps(self):
        timestamp = datetime.now().strftime("%m-%d-%Y-%H%M%S")
        base_text = f"TESTING-{timestamp}"

        while True:
            # --- Select previous entry if required ---
            if self.select_previous_entry():
                continue

            step_container = self.wait.until(
                expected_conditions.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".container-question:not([style*='display: none'])")
                )
            )


            example_elements = step_container.find_elements(By.CSS_SELECTOR, ".question-example .text-grey-dark")
            example_text = example_elements[0].text.strip() if example_elements else ""
            full_text = f"{base_text} {example_text}"

            text_areas = step_container.find_elements(By.TAG_NAME, "textarea")
            if text_areas:
                time.sleep(1)
                text_areas[0].clear()
                text_areas[0].send_keys(full_text)

            checkboxes = step_container.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            if checkboxes:
                time.sleep(1)
                random.choice(checkboxes).click()

            submit_buttons = step_container.find_elements(By.CSS_SELECTOR, "button[type='submit']")
            if submit_buttons:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_buttons[0])
                self.wait.until(lambda d: submit_buttons[0].is_displayed() and submit_buttons[0].is_enabled())
                time.sleep(1)
                submit_buttons[0].click()
                break

            next_buttons = step_container.find_elements(By.CSS_SELECTOR, ".btn-next")
            if next_buttons:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_buttons[0])
                self.wait.until(lambda d: next_buttons[0].is_displayed() and next_buttons[0].is_enabled())
                time.sleep(1)
                next_buttons[0].click()
            else:
                break

    def has_media(self):
        return bool(self.driver.find_elements(By.CSS_SELECTOR, "video, audio"))

    def play_media(self):
        media = self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "video, audio"))
        )
        self.driver.execute_script("arguments[0].play();", media)
        time.sleep(3)
        assert self.driver.execute_script("return !arguments[0].paused;", media)

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

        # submit_button = self.wait.until(
        #     expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "form.form-completed-survey button[type='submit']"))
        # )
        #
        # submit_button.click()

        self.click_element(By.CSS_SELECTOR, "form.form-completed-survey button[type='submit']")

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
        # next_button = self.wait.until(
        #     expected_conditions.element_to_be_clickable(
        #         (By.CSS_SELECTOR, ".container-program-progress-footer .item-program-progress.next a")
        #     )
        # )
        #
        # # 4: Click next button
        # next_button.click()
        self.click_element(By.CSS_SELECTOR, ".container-program-progress-footer .item-program-progress.next a")

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

        self.click_element(By.CSS_SELECTOR, "form.form-goal-survey button[type='submit']")
        # submit_button = self.wait.until(
        #     expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "form.form-goal-survey button[type='submit']"))
        # )
        #
        # submit_button.click()


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
    def __init__(self, tile):
        self.tile = tile

    @property
    def title(self):
        return self.tile.find_element(By.CSS_SELECTOR, ".title").text.strip()

    @property
    def status(self):
        badges = self.tile.find_elements(By.CSS_SELECTOR, ".badge-container .badge")
        if not badges:
            return None
        classes = badges[0].get_attribute("class")
        if "badge-complete" in classes:
            return "COMPLETED"
        if "badge-in-progress" in classes:
            return "IN-PROGRESS"
        return None

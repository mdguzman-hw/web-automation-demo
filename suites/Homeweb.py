import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from core.BasePage import BasePage
from core.Constants import HOMEWEB_BASE_URL, HOMEWEB_DOMAIN, SENTIO_DOMAIN, LIFESTAGE_DOMAIN, LIFESTYLE_DOMAIN
from core.Header import Header
from selenium.webdriver.support import expected_conditions

from core.Public import Public


class Homeweb(BasePage):
    # Properties
    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def domain(self):
        return HOMEWEB_DOMAIN

    def __init__(self, driver, language):
        super().__init__(driver, language)
        self.base_url = HOMEWEB_BASE_URL
        self.landing_url = HOMEWEB_BASE_URL + "/" + language
        self.public = Public.EN if language == "en" else Public.FR
        self._is_authenticated = False
        self._is_landing = False
        self.header = None
        self.update_header()

    # Methods
    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="homeweb", language=self.language, user=user_type)

    def navigate_landing(self):
        self.driver.get(f"{self.base_url}/{self.language}")
        self.set_landing(True)

    def go_back(self):
        self.driver.back()
        self.wait.until(
            lambda d: "homeweb.ca" in d.current_url
        )
        self.driver.execute_script("window.scrollBy(0, 0);")

    def set_landing(self, value):
        self._is_landing = value

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()

    def is_authenticated(self):
        return self._is_authenticated

    def is_landing(self):
        return self._is_landing

    def wait_for_dashboard(self):
        expected_path = f"/app/{self.language}/homeweb/dashboard"

        self.set_landing(False)

        self.set_authenticated(True)

        return self.wait.until(
            lambda d: HOMEWEB_DOMAIN in d.current_url.lower() and expected_path in d.current_url.lower()
        )

    def wait_for_resource_content(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#container-manager"))
        )

    def wait_for_sentio_transfer(self):
        return self.wait.until(
            lambda d: SENTIO_DOMAIN in d.current_url.lower() and "/sso/token" in d.current_url.lower()
        )

    def wait_for_lifestage_transfer(self):
        return self.wait.until(
            lambda d: LIFESTAGE_DOMAIN in d.current_url.lower()
        )

    def wait_for_lifestyle_transfer(self):
        return self.wait.until(
            lambda d: LIFESTYLE_DOMAIN in d.current_url.lower()
        )

    def wait_for_modal(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )

    def wait_for_course_content(self):
        # 1: Locate embed container
        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "iframeWrapper"))
        )

        # 2: Locate and switch to iframe content
        iframe = self.wait.until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        self.driver.switch_to.frame(iframe)

        # 3: Wait for main slide to appear inside iframe
        self.wait.until(expected_conditions.visibility_of_element_located((By.ID, "div_Slide")))

        # 4: Wait until all immediate child elements of the slide are visible
        self.wait.until(lambda d: d.execute_script("""
                const slide = document.getElementById('div_Slide');
                if (!slide) return false;
                return Array.from(slide.children).some(c => {
                    const style = window.getComputedStyle(c);
                    const rect = c.getBoundingClientRect();
                    return style.display !== 'none' &&
                           style.visibility !== 'hidden' &&
                           rect.width > 0 &&
                           rect.height > 0;
                });
            """))

        # 5: Additional check to user interaction is permitted
        self.wait.until(
            expected_conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, "#blockUserInteraction.loadingBackground")
            )
        )

        # 6: Switch back to main content
        self.driver.switch_to.default_content()
        return True

    def wait_for_logout(self):
        # KNOWN ISSUE 1: Logout will always go to EN Landing

        self.set_landing(True)
        self.set_authenticated(False)

        return self.wait.until(
            lambda d: self.base_url + "/en" in d.current_url.lower()
        )

    def get_articles(self):
        # 1: Find articles container
        self.wait.until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "row-cards")
            )
        )

        # 2: Find all articles in container
        article_elements = self.wait.until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, ".row-cards .card-container"))
        )

        # 3: Store article titles and href into an array
        articles = []
        for article in article_elements:
            title = article.find_element(By.CLASS_NAME, "card-title").text
            href = article.find_element(By.CSS_SELECTOR, "a[role='button']").get_attribute("href")

            articles.append({
                "title": title,
                "href": href
            })

        # 4: Return array of articles
        return articles

    def get_active_appointments(self):
        # 1: Find Active appointments container
        appointments_zone = self.driver.find_elements(By.CSS_SELECTOR, ".zone-appointments")

        # 1.1: No active appointments
        if not appointments_zone:
            print("No active appointments")
            return []

        # 1.2: Retrieve active appointments
        appointment_tiles = appointments_zone[0].find_elements(By.CSS_SELECTOR, ".item-booking-v2")
        return [AppointmentTile(tile) for tile in appointment_tiles]

    def end_services(self, topic):
        done_text = "Oui j'ai terminé" if self.language == "fr" else "Yes, I am done"

        # 1: Locate appointment tile by topic
        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".zone-appointments"))
        )
        appointment_tile = self.driver.find_element(
            By.XPATH,
            f'//p[normalize-space()="{topic}"]/ancestor::div[contains(@class,"item-booking-v2")]'
        )

        # 2: Within the appointment tile, find and scroll to end services link, if required
        end_services_link = appointment_tile.find_element(By.CLASS_NAME, "btn-link")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            end_services_link
        )
        time.sleep(0.5)

        # 3: Click end services within tile
        self.wait.until(expected_conditions.element_to_be_clickable(end_services_link))
        end_services_link.click()

        # 4: Click Yes, I am done within tile
        done_btn = self.wait.until(expected_conditions.element_to_be_clickable(
            (By.LINK_TEXT, done_text)
        ))
        done_btn.click()

        # 5: Confirm end services
        self.wait.until(expected_conditions.url_contains("/services/end"))
        self.click_element(By.CSS_SELECTOR, "button.cancel-confirm")

        # 6: Complete end service survey
        self.complete_end_service_survey()

    def complete_end_service_survey(self):
        radios = self.wait.until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "form.form-end-service input[type='radio']")
            )
        )
        random.choice(radios).click()

    # TODO: Implement for Sentio Beta - Client Suite once test criterias have been finalized
    def test_live_chat(self, email):
        # TODO: Find a stronger fail criteria. No avaialble agents message?
        chat_btn_locator = "svelte-mffmc3"
        email_input_locator = "inputLabel-courriel" if self.language == "fr" else "inputLabel-email"
        begin_chat_locator = "[data-selector='PRIMARY_BUTTON']"

        # 1: Locate Live Chat button and click it
        self.wait.until(expected_conditions.element_to_be_clickable(
            (By.CLASS_NAME, chat_btn_locator)
        ))
        self.click_element(By.CLASS_NAME, chat_btn_locator)

        # 2: Locate iFrame window and switch to it
        self.wait.until(
            expected_conditions.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='Customer Chat']"))
        )

        # 3. Locate inputs
        name_input = self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, "inputLabel-name"))
        )
        assert name_input.is_displayed()
        name_value = name_input.get_attribute("value").strip()

        email_input = self.wait.until(
            expected_conditions.visibility_of_element_located((By.ID, email_input_locator))
        )
        assert email_input.is_displayed()
        email_value = email_input.get_attribute("value").strip()

        # 4: Assert that name and email fields are filled out
        if not name_value:
            name_input.clear()
            name_input.send_keys(email.split("@")[0])
        print(f"NAME -> {name_value}")

        if not email_value:
            email_input.clear()
            email_input.send_keys(email)
        print(f"EMAIL -> {email_value}")

        assert name_value != ""
        assert email_value != ""

        # 5: Assert Begin Chat button exists and click it
        begin_chat_button = self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, begin_chat_locator))
        )
        assert begin_chat_button.is_displayed()
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            begin_chat_button
        )
        self.driver.execute_script("arguments[0].click();", begin_chat_button)

        # 6: Wait for chat scrollbox
        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "div.ScrollBox_content__2fOBG"))
        )
        print("CHAT SCROLLBOX FOUND. Waiting for agent to join the chat")

        # 7: Wait for agent join system message (EN)
        long_wait = WebDriverWait(self.driver, 180)  # 180 seconds = 3 minutes
        agent_join_msg = long_wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "span[data-selector='SYSTEM_MESSAGE_CONTENT']")
            )
        )
        assert "has joined the chat" in agent_join_msg.text.strip()
        print("CHAT AGENT HAS JOINED.")

        # 8: Wait for first agent message
        first_agent_msg = self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div[data-selector='AGENT_MESSAGE_BUBBLE'] span.Linkify")
            )
        )
        print(f"CHAT AGENT FIRST REPLY CONFIRMED -> {first_agent_msg.text.strip()}. Press enter to continue...")

        # 9: Locate reply textarea
        reply_box = self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "textarea[data-selector='TEXTAREA']"))
        )

        # 10: Send first automated message
        reply_box.send_keys("Automated Test Message. Please reply to confirm message has been received.\n")

        # 11: Wait for agent reply
        medium_wait = WebDriverWait(self.driver, 60)  # 60 seconds = 1 minute
        medium_wait.until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, "div[data-selector='AGENT_MESSAGE_BUBBLE']")[-1].text != first_agent_msg.text
        )

        # 12: Send confirmation message
        reply_box.send_keys("Chat reply confirmed. You may now close this chat session. Thank you.\n")

        # 13: Wait for chat session end
        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "div.EndSession_Footer__RE+Xe"))
        )

        input("LIVE CHAT TEST SESSION ENDED. Press enter to continue...")


class AppointmentTile:
    def __init__(self, tile):
        self._tile = tile

    @property
    def topic(self):
        return self._tile.find_element(By.CSS_SELECTOR, ".h4.font-semibold").text.strip()

    @property
    def date_time(self):
        return self._tile.find_element(By.CSS_SELECTOR, ".appointment-date-time").text.strip()

    @property
    def provider(self):
        return self._tile.find_element(By.CSS_SELECTOR, ".column-provider-details .name").text.strip()

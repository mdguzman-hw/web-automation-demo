# Copyright © 2026 - Homewood Health Inc.

import random
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from core.BasePage import BasePage
from core.Constants import HOMEWEB_BASE_URL, HOMEWEB_DOMAIN, SENTIO_DOMAIN, LIFESTAGE_DOMAIN, LIFESTYLE_DOMAIN, HOMEWEB_BETA_BASE_URL, HOMEWEB_BETA_DOMAIN
from core.Header import Header
from selenium.webdriver.support import expected_conditions

from core.Public import Public


class Homeweb(BasePage):
    @property
    def current_url(self):
        return self.driver.current_url

    def __init__(self, driver, language, env, quantum):
        super().__init__(driver, language)

        if env == "prod":
            self.base_url = HOMEWEB_BASE_URL
            self.domain = HOMEWEB_DOMAIN
        else:
            self.base_url = HOMEWEB_BETA_BASE_URL
            self.domain = HOMEWEB_BETA_DOMAIN

        self.quantum = quantum
        self.landing_url = self.base_url + "/" + language
        self.public = Public.EN if language == "en" else Public.FR
        self._is_authenticated = False
        self._is_landing = False
        self.header = None
        self.update_header()

    # Methods
    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="homeweb", language=self.language, user=user_type)

    def navigate_landing(self, custom=None):
        if custom:
            self.driver.get(f"{self.base_url}/{self.language}/{custom}")
        else:
            self.driver.get(f"{self.base_url}/{self.language}")

        self.set_landing(True)

    def navigate_dashboard(self):
        self.click_element(By.CSS_SELECTOR, self.header.elements["buttons"]["dashboard"])

    def navigate_resources(self):
        self.click_element(By.CSS_SELECTOR, self.header.elements["buttons"]["resources"])

    def wait_for_resources(self):
        resources_endpoint = "/resources"
        self.wait.until(lambda d: resources_endpoint in d.current_url.lower())

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "col-category-sidebar"))
        )

        return True
    def wait_for_resources(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "nav.category-nav"))
        )

    def get_resource_categories(self):
        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "nav.category-nav > ul > li > a"))
        )
        return self.driver.find_elements(By.CSS_SELECTOR, "nav.category-nav > ul > li > a")

    def get_resource_subcategories(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "nav.category-nav .child-nav li a")

    def search_resources(self, query: str):
        search_input = self.wait.until(
            expected_conditions.element_to_be_clickable((By.ID, "searchHomeweb"))
        )
        search_input.clear()
        search_input.send_keys(query)
        self.click_element(By.ID, "search")

    def wait_for_search_results(self):
        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "resource-count"))
        )
        return True

    def navigate_recommendations(self):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "item-pathfinder-recommends-v2")))
        self.click_element(By.CSS_SELECTOR, "div.item-pathfinder-recommends-v2 a")

    def navigate_rating(self):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "section-recommendations")))
        link_text = "Commencer Maintenant" if self.language == "fr" else "Get started"
        self.click_element(By.LINK_TEXT, link_text)

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

    def wait_for_landing(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "container-page-dynamic"))
        )

    def wait_for_dashboard(self):
        expected_path = f"/app/{self.language}/homeweb/dashboard"

        self.set_landing(False)

        self.set_authenticated(True)

        # self.

        return self.wait.until(
            lambda d: HOMEWEB_DOMAIN in d.current_url.lower() and expected_path in d.current_url.lower()
        )

    def wait_for_resource_content(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#container-manager"))
        )

    def wait_for_sentio_transfer(self):
        return self.wait.until(lambda d: SENTIO_DOMAIN in d.current_url.lower() and "/sso/token" in d.current_url.lower())

    def wait_for_lifestage_transfer(self):
        return self.wait.until(lambda d: LIFESTAGE_DOMAIN in d.current_url.lower())

    def wait_for_lifestyle_transfer(self):
        return self.wait.until(lambda d: LIFESTYLE_DOMAIN in d.current_url.lower())

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

    def wait_for_assessment(self):
        assessment_endpoint = "pathfinder/assessment"
        self.wait.until(lambda d: assessment_endpoint in d.current_url.lower())

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "section-assessment"))
        )

        return True

    def wait_for_recommendation(self):
        recommendation_endpoint = "pathfinder/assessment/recommendation"
        self.wait.until(lambda d: recommendation_endpoint in d.current_url.lower())

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "section-recommendations"))
        )

        return True

    def wait_for_rating(self):
        recommendation_endpoint = "pathfinder/assessment/rating"
        self.wait.until(lambda d: recommendation_endpoint in d.current_url.lower())

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "section-five-star-rating"))
        )

        return True

    def wait_for_booking_create(self):
        booking_create_endpoint = "homeweb/booking/create"
        self.wait.until(lambda d: booking_create_endpoint in d.current_url.lower())

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "container-case-creation"))
        )

        return True

    def wait_for_service_confirm(self):
        service_confirm_endpoint = "homeweb/services/confirm"
        self.wait.until(lambda d: service_confirm_endpoint in d.current_url.lower())

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "container-confirm"))
        )

        return True

    def wait_for_booking_digest(self):
        booking_digest_endpoint = "homeweb/booking"
        self.wait.until(lambda d: booking_digest_endpoint in d.current_url.lower())

        self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "collection-provider-matches"))
        )

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "dp__instance_calendar"))
        )

        return True

    def wait_for_booking_details(self):
        booking_digest_endpoint = "homeweb/booking/detail"
        self.wait.until(lambda d: booking_digest_endpoint in d.current_url.lower())

        self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "section-booking"))
        )

        return True

        # TODO TEST: Resource Libraru
        # def wait_for_resources(self):
        #     resources_endpoint = "/resources"
        #     self.wait.until(lambda d: resources_endpoint in d.current_url.lower())
        #
        #     self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))
        #
        #     self.wait.until(
        #         expected_conditions.visibility_of_element_located((By.CLASS_NAME, "controller-content"))
        #     )
        #
        #     expected_active = "Santé mentale" if self.language == "fr" else "Mental Health"
        #     active_item = self.driver.find_element(By.CSS_SELECTOR, "#categoryNav li.active > a").text.strip()
        #     print (active_item)
        #     assert expected_active in active_item

        return True

    def wait_for_booking_confirm(self):
        booking_confirm_endpoint = "/homeweb/booking/confirm"
        self.wait.until(lambda d: booking_confirm_endpoint in d.current_url.lower())

        self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "dsg-inner"))
        )

        return True

    def wait_for_pulsecheck(self):
        pulsecheck_endpoint = "wellness/pulsecheck"

        self.wait.until(lambda d: pulsecheck_endpoint in d.current_url.lower())

        self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))

        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "pulsecheck-slide"))
        )

        return True

    # def wait_for_booking_confirmation(self):
    #     booking_confirmation_endpoint = "/homeweb/booking/confirm"
    #     self.wait.until(lambda d: booking_confirm_endpoint in d.current_url.lower())
    #
    #     self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))
    #
    #     self.wait.until(
    #         expected_conditions.visibility_of_element_located((By.CLASS_NAME, "dsg-inner"))
    #     )
    #
    #     return True

    def complete_enbridge_login_modal(self):
        self.wait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )

        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-block a.btn")
        # TODO: Investigate duplicate modal-content
        # print(len(buttons))
        print(buttons[0].text.strip()) # United States
        print(buttons[1].text.strip()) # Canada
        # print(buttons[2].text.strip()) # EMPTY??
        # print(buttons[3].text.strip()) # EMPTY??
        # for button in buttons:
        #     print()
        self.wait.until(expected_conditions.element_to_be_clickable(buttons[1]))
        buttons[1].click()

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

    def get_active_services(self):
        # 1: Find Active appointments container
        appointments_zone = self.driver.find_elements(By.CSS_SELECTOR, ".zone-appointments")

        # 1.1: No active appointments
        if not appointments_zone:
            print("No active services")
            return []

        # 1.2: Retrieve active appointments
        appointment_tiles = appointments_zone[0].find_elements(By.CSS_SELECTOR, ".item-booking-v2")
        return [AppointmentTile(tile) for tile in appointment_tiles]

    def get_dashboard_tiles(self):
        # TODO: Investigate if this is expected
        zone_length = "6" if self.language == "fr" else "8"
        selector = f"div.collection.collection-dashboard.zone-length-{zone_length} .item"
        tile_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        tiles = []

        for tile in tile_elements:
            title = tile.find_element(By.CSS_SELECTOR, ".item-content h3.title").text.strip()
            href = tile.find_element(By.CSS_SELECTOR, ".item-content a.item-link").get_attribute("href")
            link_text = tile.find_element(By.CSS_SELECTOR, ".item-content a.item-link").text.strip()
            tiles.append(DashboardTile(self.driver, self.wait, tile, title, href, link_text))
        return tiles

    def get_primary_categories(self):
        category_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav.category-nav > ul > li > a")
        return category_elements
        # category_element = self.wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "nav.category-nav li a")))

        # categories = []
        # primary_items = self.driver.find_elements(By.CSS_SELECTOR, "#categoryNav > ul > li")
        #
        # for item in primary_items:
        #     title = item.find_element(By.CSS_SELECTOR, "a").text.strip()
        #     subcategories = [
        #         sub.text.strip()
        #         for sub in item.find_elements(By.CSS_SELECTOR, ".child-nav li a")
        #     ]
        #     categories.append({"title": title, "subcategories": subcategories})
        #
        # return categories

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

    def test_live_chat(self, email):
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

        # 7: Wait for agent join system message
        # 2 min max wait time -> Match ring central Available Agent Search Time
        long_wait = WebDriverWait(self.driver, 120)
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
        medium_wait = WebDriverWait(self.driver, 60)
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

    def get_current_question(self):
        self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".assessment-question-text h3")
            )
        )

        assessment_question = self.driver.find_element(
            By.CSS_SELECTOR,
            ".assessment-question-text h3"
        ).text.strip()

        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "option")))
        options = self.driver.find_elements(By.CLASS_NAME, "option")
        assessment_options = []

        for option in options:
            label = option.find_element(By.CSS_SELECTOR, "button.btn-answer")
            assessment_options.append(label)

        return assessment_question, assessment_options

    def is_assessment_complete(self):
        return "/assessment/recommendation" in self.driver.current_url

    def get_recommendations(self):
        recommendation_tiles = self.driver.find_elements(By.CLASS_NAME, "item-pathfinder-recommends-v2")
        # for tile in recommendation_tiles:
        #     print(tile.text.strip())
        return recommendation_tiles

    def _recommendation_texts(self):
        return [tile.text.strip() for tile in self.get_recommendations()]

    def _has_recommendation(self, text):
        return any(text in t for t in self._recommendation_texts())

    @property
    def _support_text(self):
        return "Un soutien professionnel" if self.language == "fr" else "Professional Support"

    @property
    def _icbt_text(self):
        return "La TCC en ligne Sentio" if self.language == "fr" else "Sentio iCBT"

    def assert_recommendation_scenario_1(self):
        """Scenario 1: Professional Support AND Sentio iCBT"""
        assert self._has_recommendation(self._support_text), f"Expected '{self._support_text}' tile"
        assert self._has_recommendation(self._icbt_text), f"Expected '{self._icbt_text}' tile"

    def assert_recommendation_scenario_2(self):
        """Scenario 2: Sentio iCBT only"""
        assert self._has_recommendation(self._icbt_text), f"Expected '{self._icbt_text}' tile"
        assert not self._has_recommendation(self._support_text), f"Did not expect '{self._support_text}' tile"

    def assert_recommendation_scenario_3(self):
        """Scenario 3: Professional Support only"""
        assert self._has_recommendation(self._support_text), f"Expected '{self._support_text}' tile"
        assert not self._has_recommendation(self._icbt_text), f"Did not expect '{self._icbt_text}' tile"

    def wait_for_next_step(self, previous_question):
        self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))

        def condition(driver):
            # case 1: completed
            if self.is_assessment_complete():
                return True

            # case 2: new question
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".assessment-question-text h3")
            if elements:
                return elements[0].text.strip() != previous_question
            return False

        self.wait.until(condition)

    def complete_assessment(self, flow=None, answer_index=0):
        """
        Complete the assessment by selecting an answer on each question.

        flow         : list of int — answer indices to follow in order (e.g. [0, 1, 0, 2])
                                     falls back to answer_index when the list is exhausted
        answer_index : int         — fallback answer position when no flow is given or flow runs out
                     : "random"    — pick a random answer as the fallback
        """
        step = 0
        used_flow = []

        while not self.is_assessment_complete():
            question_text, answers = self.get_current_question()

            if flow and step < len(flow):
                index = flow[step]
            elif answer_index == "random":
                index = random.randrange(len(answers))
            else:
                index = answer_index

            selected = answers[min(index, len(answers) - 1)]
            used_flow.append(index)

            print(f"Q{step + 1}: [{index}] {selected.text.strip()}")

            self.wait.until(
                expected_conditions.element_to_be_clickable(selected)
            ).click()
            self.wait_for_next_step(question_text)
            step += 1

        return used_flow

    def complete_rating(self, rating=None):
        if rating is not None:
            selected = self.wait.until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'#rating-form label[for="{rating}"]')
                )
            )
        else:
            options = self.driver.find_elements(By.CSS_SELECTOR, f"#rating-form label")
            selected = random.choice(options)

        self.wait.until(expected_conditions.element_to_be_clickable(selected))
        selected.click()

    def complete_booking_create_form(self):
        # 1: Wait for form to load
        self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.controller-content form")
            )
        )

        # 2: Street Address
        address = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "streetAddress")))
        address.clear()
        address.send_keys("6767 Homewood Street")

        # 3: Province
        province_select = Select(self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "provinceState"))))
        province_options = [o.text for o in province_select.options if o.get_attribute("value")]
        current_province = province_select.first_selected_option.text
        current_cities = [o.text for o in self.driver.find_element(By.ID, "city").find_elements(By.TAG_NAME, "option")]
        selected_province = random.choice(province_options)
        province_select.select_by_visible_text(selected_province)
        print(selected_province)

        # 4: City (wait for reload only if province changed)
        from selenium.common.exceptions import StaleElementReferenceException

        if selected_province != current_province:
            def city_reloaded(driver):
                try:
                    return [o.text for o in driver.find_element(By.ID, "city").find_elements(By.TAG_NAME, "option")] != current_cities
                except StaleElementReferenceException:
                    return False

            self.wait.until(city_reloaded)

        # if selected_province != current_province:
        #     self.wait.until(lambda d: [o.text for o in d.find_element(By.ID, "city").find_elements(By.TAG_NAME, "option")] != current_cities)

        city_select = Select(self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "city"))))
        city_options = [o.text for o in city_select.options if o.get_attribute("value")]
        selected_city = random.choice(city_options)
        city_select.select_by_visible_text(selected_city)
        print(selected_city)

        # 5: Postal Code
        postal = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "postalZipCode")))
        postal.clear()
        postal.send_keys("T6V7X3")

        # 6: Phone Number
        phone = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "phoneNumber")))
        phone.clear()
        phone.send_keys("9876543210")

        # 7: Message Permission
        # messageOk
        # discreetMessage
        # noMessage
        self.click_element(By.ID, "noMessage")

        # 8: Comments
        phone = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "comments")))
        phone.clear()
        timestamp = datetime.now().strftime("%m-%d-%Y-%H%M%S")
        base_text = f"TEST COMMENT-{timestamp}"
        phone.send_keys(base_text)

        # 9: Submit
        self.click_element(By.CSS_SELECTOR, "button.submit-inner")

    def complete_service_confirm_form(self, email):
        # 1: Wait for form to load
        self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, "container-confirm")
            )
        )

        # 2: Email
        email_field = self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(email)
        print(email)

        self.click_element(By.CSS_SELECTOR, "button[type='submit']")

    def continue_booking(self, topic):
        continue_text = "Reprendre la prise du rendez-vous" if self.language == "fr" else "Continue to Booking"

        tile = self.driver.find_element(
            By.XPATH,
            f'//p[normalize-space()="{topic}"]/ancestor::div[contains(@class,"item-booking-v2")]'
        )
        continue_link = tile.find_element(By.LINK_TEXT, continue_text)
        # print(f"CONTINUE FOUND -> {continue_link}")
        self.click_element(By.LINK_TEXT, continue_text)
        # self.wait.until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, continue_text)))
        # continue_link.click()

    def get_booking_options(self):
        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".section-suggestions .item-booking-option"))
        )

        tiles = self.driver.find_elements(By.CSS_SELECTOR, ".section-suggestions .item-booking-option")
        return [ProviderTile(tile) for tile in tiles]

    # TODO: Select provider w/ time
    def select_provider_time(self):
        booking_options = self.get_booking_options()
        # self.click_element()
        # selected_option = random.choice(booking_options)
        # print(f"Selected provider: {selected_option.provider_name}")
        # selected_time = selected_option.select_random_time()
        # print(f"Selected time: {selected_time}")

    def select_provider(self):
        booking_options = self.get_booking_options()
        selected_option = random.choice(booking_options)
        print(selected_option.provider_name)
        link = selected_option.provider_details_link
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        time.sleep(0.5)
        self.wait.until(expected_conditions.element_to_be_clickable(link))
        link.click()

    def select_booking_options(self):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "section-booking")))

        # 2: Select a random available time
        time_options = self.wait.until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".provider-times-container label.btn-time")
            )
        )
        selected_time = random.choice(time_options)
        print(selected_time.text.strip())
        selected_time.click()

        # 3: Wait for modality select to enable after time selection
        self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "appointmentModality")))
        modality_select = Select(self.driver.find_element(By.ID, "appointmentModality"))
        modality_options = [o.text for o in modality_select.options if o.get_attribute("value") != "0"]
        selected_modality = random.choice(modality_options)
        print(selected_modality)
        modality_select.select_by_visible_text(selected_modality)

        # 4: Click Review & confirm
        self.click_element(By.CSS_SELECTOR, "button.btn-primary:not(.disabled)")

    def confirm_booking(self):
        self.driver.find_elements(By.CLASS_NAME, "btn-booking")

        yes_button = self.wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "div.container-buttons button"))
        )

        yes_button.click()

        self.wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loadingPage")))
        # print("PAGE LOADED")

        # TODO: Assert Continue to Booking button is no longer visible on Dashboard
        # NOTE: Booking Confirmed at this point - Sufficient for now. See Additional Tests Below
        # Additional Tests
        # TEST: Confirmation Method
        # homeweb.choose_confirmation_method()

    def choose_confirmation_method(self, method="text"):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "container-buttons")))

        buttons = self.driver.find_elements(By.CLASS_NAME, "btn-booking")
        print(len(buttons))

        # if method == "text":
        #     buttons[0].click()
        # else:
        #     buttons[1].click()


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


# Dashboard Tiles - EN
# 0 - Pathfinder
# 1 - Sentio by Homewood Health
# 2 - Resource Library
# 3 - How are you doing today?
# 4 - Childcare Resource Locator by LifestageCare
# 5 - Eldercare Resource Locator by LifestageCare
# 6 - Health and Wellness Library
# 7 - Health Risk Assessment
class DashboardTile:
    def __init__(self, driver, wait, tile, title, href, link_text):
        self.driver = driver
        self.wait = wait
        self.tile = tile
        self.title = title
        self.href = href
        self.link_text = link_text

    def navigate(self):
        link = self.tile.find_element(By.LINK_TEXT, self.link_text)

        # scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", link
        )

        # 3: Wait for layout to stabilize
        self.wait.until(lambda d: link.is_displayed() and link.is_enabled())

        # 4: Small pause to allow any final reflows
        time.sleep(0.5)
        # wait until clickable
        clickable_element = self.wait.until(expected_conditions.element_to_be_clickable(link))

        clickable_element.click()


class ProviderTile:
    def __init__(self, tile):
        self._tile = tile

    @property
    def provider_name(self):
        return self._tile.find_element(By.CSS_SELECTOR, "a.provider-name").text.strip()

    @property
    def provider_details_link(self):
        return self._tile.find_element(By.CSS_SELECTOR, "a.link-provider-details")

    @property
    def available_times(self):
        return self._tile.find_elements(By.CSS_SELECTOR, ".provider-times-container .btn-time")

    def select_random_time(self):
        times = self.available_times
        random.choice(times).click()

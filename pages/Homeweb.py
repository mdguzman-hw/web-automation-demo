from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
from pages.Constants import HOMEWEB_BASE_URL, HOMEWEB_DOMAIN, SENTIO_DOMAIN, LIFESTAGE_DOMAIN, LIFESTYLE_DOMAIN
from pages.Header import Header
from selenium.webdriver.support import expected_conditions

from pages.Public import Public


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

################# BUILD ACCEPTANCE ################
############# SENTIO BETA - PROVIDER ##############
from selenium.webdriver.common.by import By


# TEST: Navigate Sentio Beta - Provider
def test_bat_web_024(sentio_provider):
    sentio_provider.driver.get(sentio_provider.base_url)
    quantum = sentio_provider.quantum
    print(f"MDG::Testing->{quantum.domain}")
    assert quantum.domain in sentio_provider.current_url.lower()


# TEST: Sentio Beta Provider Login
def test_bat_web_025(sentio_provider, credentials):
    quantum = sentio_provider.quantum

    assert quantum.domain in quantum.current_url.lower()
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert sentio_provider.wait_for_login()


# TEST: New Dashboard
def test_bat_web_026(sentio_provider):
    assert sentio_provider._is_authenticated

    # Login always navigates to EN, need to toggle to french manually after login
    header = sentio_provider.header
    header_elements = header.elements
    if sentio_provider.language == "fr":
        header.click_element(By.CSS_SELECTOR, ".btn.btn-nav-item.btn-language.btn-icon-spaced")

    assert sentio_provider.wait_for_dashboard("classic")

    header.click_element(By.CSS_SELECTOR, header_elements["new"])
    assert sentio_provider.wait_for_dashboard("new")


# TEST: Sentio Beta Provider Logout
def test_bat_web_027(sentio_provider):
    assert sentio_provider._is_authenticated

    header = sentio_provider.header
    header_buttons = header.elements["buttons"]
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    header.click_element(By.CSS_SELECTOR, header_buttons["menu_sign_out"])
    quantum = sentio_provider.quantum
    assert quantum.domain in sentio_provider.current_url.lower()

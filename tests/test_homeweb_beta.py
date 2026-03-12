################# BUILD ACCEPTANCE ################
################## HOMEWEB BETA ###################
from selenium.webdriver.common.by import By


# TEST: Navigate Homeweb
def test_bat_web_001_beta(homeweb_beta):
    # 1: Test - Navigate to Homeweb landing
    homeweb_beta.navigate_landing()
    assert homeweb_beta.domain in homeweb_beta.current_url.lower()


# TEST: Homeweb Landing Articles
def test_bat_web_002_beta(homeweb_beta):
    assert homeweb_beta.is_landing()
    articles = homeweb_beta.get_articles()

    # 1: Test - Resources 1-3 (Dynamic articles -> subject to change)
    for article in articles:
        locator = f'//h3[contains(normalize-space(), "{article["title"]}")]//ancestor::div[contains(@class,"card-container")]//a[@role="button"]'
        homeweb_beta.click_element(By.XPATH, locator)
        assert article["href"] in homeweb_beta.current_url.lower()
        assert homeweb_beta.wait_for_resource_content()
        homeweb_beta.go_back()

    # 2: Test - Resource 4 (Static article)
    resources = homeweb_beta.public["elements"]["resources"]
    paths = homeweb_beta.public["paths"]["resources"]
    homeweb_beta.click_element(By.LINK_TEXT, resources["toolkit"])
    assert paths["toolkit"] in homeweb_beta.current_url.lower()
    assert homeweb_beta.wait_for_resource_content()
    homeweb_beta.go_back()


# TEST: Homeweb Login
def test_bat_web_003_beta(homeweb_beta, quantum_api_beta, credentials):
    assert homeweb_beta.is_landing()
    buttons = homeweb_beta.public["elements"]["buttons"]

    # 1: Test - Sign In - Button
    homeweb_beta.click_element(By.XPATH, buttons["sign_in"])
    assert quantum_api_beta.domain in quantum_api_beta.current_url.lower()

    # 2: Test - Login - Homeweb - Personal
    quantum_api_beta.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert homeweb_beta.wait_for_dashboard()


# TEST: Homeweb Resource
def test_bat_web_004_beta(homeweb_beta):
    assert homeweb_beta.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = homeweb_beta.base_url + "/" + homeweb_beta.language + "/user/articles/56252b81e40e6f50062aa714"
    homeweb_beta.driver.get(resource_target)
    assert homeweb_beta.wait_for_resource_content()


# TEST: Sentio kick-out
def test_bat_web_005_beta(homeweb_beta):
    assert homeweb_beta.is_authenticated()

    # 1: Navigate to sentio resource
    sentio_resource_target = homeweb_beta.base_url + "/app/" + homeweb_beta.language + "/resources/62c5a1e929ed9c1608d0434b"
    homeweb_beta.driver.get(sentio_resource_target)
    assert homeweb_beta.wait_for_resource_content()

    # 2: Test - Sentio transfer kickout
    homeweb_beta.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb_beta.wait_for_sentio_transfer()
    homeweb_beta.go_back()


# TEST: Homeweb Logout
def test_bat_web_006_beta(homeweb_beta):
    assert homeweb_beta.is_authenticated()
    header = homeweb_beta.header
    header_buttons = header.elements["buttons"]

    # 1: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 2: Test - Logout
    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb_beta.wait_for_logout()
    homeweb_beta.navigate_landing()


# TEST: Homeweb Login - Different user
def test_bat_web_007_beta(homeweb_beta, quantum_api_beta, credentials):
    assert homeweb_beta.is_landing()
    header = homeweb_beta.header
    header_buttons = header.elements["buttons"]
    paths = header.paths["buttons"]

    # 1: Test - Sign In - Header
    header.click_element(By.CLASS_NAME, header_buttons["sign_in"])
    assert paths["sign_in"] in quantum_api_beta.current_url.lower()

    # 2: Test - Login - Homeweb - DSG Demo
    quantum_api_beta.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert homeweb_beta.wait_for_dashboard()


# TEST: Kickouts
def test_bat_web_008_beta(homeweb_beta, quantum_api_beta, credentials):
    assert homeweb_beta.is_authenticated()

    childcare_resource_target = homeweb_beta.base_url + "/app/" + homeweb_beta.language + "/resources/579ba4db88db7af01fe6ddd4"
    eldercare_resource_target = homeweb_beta.base_url + "/app/" + homeweb_beta.language + "/resources/579ba49a88db7af01fe6ddc8"
    hra_resource_target = homeweb_beta.base_url + "/app/" + homeweb_beta.language + "/resources/579ba53088db7af01fe6dde6"

    # 1: Test - ChildCare - Lifestage transfer kickout
    homeweb_beta.driver.get(childcare_resource_target)
    assert homeweb_beta.wait_for_resource_content()
    homeweb_beta.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb_beta.wait_for_lifestage_transfer()

    # 2: Test - ElderCare - Lifestage transfer kickout
    homeweb_beta.driver.get(eldercare_resource_target)
    assert homeweb_beta.wait_for_resource_content()
    homeweb_beta.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb_beta.wait_for_lifestage_transfer()

    # 3: Test - HRA - LifeStyles transfer kickout
    homeweb_beta.driver.get(hra_resource_target)
    assert homeweb_beta.wait_for_resource_content()
    homeweb_beta.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb_beta.wait_for_lifestyle_transfer()


# TEST: Course consent
def test_bat_web_009_beta(homeweb_beta):
    assert homeweb_beta.is_authenticated()
    header = homeweb_beta.header
    header_buttons = header.elements["buttons"]

    # 1: Navigate to course
    course_target = homeweb_beta.base_url + "/app/" + homeweb_beta.language + "/resources/564a36083392100756dd3e32"
    homeweb_beta.driver.get(course_target)
    assert homeweb_beta.wait_for_resource_content()

    # 2: Test - Open modal
    homeweb_beta.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"modal\"]")
    assert homeweb_beta.wait_for_modal()

    # 3: Test - Dismiss modal, display course content
    homeweb_beta.click_element(By.CSS_SELECTOR, "[data-bs-dismiss=\"modal\"]")
    # assert homeweb.wait_for_course_content()
    assert homeweb_beta.wait_for_course_content(), "iframe content issue"

    # 4: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 5: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb_beta.wait_for_logout()

    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    homeweb_beta.navigate_landing()


# def test_bat_web_010_beta(homeweb_beta, quantum_api_beta, credentials):
#     assert homeweb_beta.is_landing()
#     header_anon = homeweb_beta.header
#     header_anon_buttons = header_anon.elements["buttons"]
#     paths = header_anon.paths["buttons"]
#
#     # 1: Test - Sign In - Header
#     header_anon.click_element(By.CLASS_NAME, header_anon_buttons["sign_in"])
#     assert paths["sign_in"] in quantum_api_beta.current_url.lower()
#
#     # 2: Test - Login - Homeweb - HHI Demo
#     quantum_api_beta.login(credentials["hhi_demo"]["email"], credentials["hhi_demo"]["password"])
#     assert homeweb_beta.wait_for_dashboard()
#
#     # 3: Test - Check and cancel active appointments
#     appointments = homeweb_beta.get_active_appointments()
#     topics = [a.topic for a in appointments]
#
#     for topic in topics:
#         homeweb_beta.end_services(topic)
#         assert homeweb_beta.wait_for_dashboard()
#         remaining = homeweb_beta.get_active_appointments()
#         assert not any(a.topic == topic for a in remaining)
#
#     # 4: Test - Menu dropdown
#     header_auth = homeweb_beta.header
#     header_auth_buttons = header_auth.elements["buttons"]
#     header_auth.click_element(By.CLASS_NAME, header_auth_buttons["menu"])
#     assert header_auth.wait_for_account_menu(), "Menu not found"
#
#     # 5: Test - Logout
#     header_auth.click_element(By.CSS_SELECTOR, header_auth_buttons["sign_out"])
#     assert homeweb_beta.wait_for_logout()
#
#     # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
#     homeweb_beta.navigate_landing()

# TODO: BAT-WEB-011 | Live Chat
# def test_bat_web_011_beta(homeweb_beta, quantum_api_beta, credentials):
#     homeweb.navigate_landing()
#     assert homeweb.domain in homeweb.current_url.lower()
#     header_anon = homeweb.header
#     header_anon_buttons = header_anon.elements["buttons"]
#     paths = header_anon.paths["buttons"]
#
#     # 1: Test - Sign In - Header
#     header_anon.click_element(By.CLASS_NAME, header_anon_buttons["sign_in"])
#     assert paths["sign_in"] in quantum.current_url.lower()
#
#     # 2: Test - Login - Homeweb - DSG Demo
#     email = credentials["sentio"]["email"]
#     quantum.login(email, credentials["sentio"]["password"])
#     assert homeweb.wait_for_dashboard()
#
#     homeweb.test_live_chat(email)


# TEST: Mobile - Embedded resources
def test_bat_web_012_beta(homeweb_beta):
    # Ensure Logged out from previous test
    # if homeweb.is_authenticated():
    #     # Test - Menu dropdown
    #     header_auth = homeweb.header
    #     header_auth_buttons = header_auth.elements["buttons"]
    #     header_auth.click_element(By.CLASS_NAME, header_auth_buttons["menu"])
    #     assert header_auth.wait_for_account_menu(), "Menu not found"
    #
    #     # Test - Logout
    #     header_auth.click_element(By.CSS_SELECTOR, header_auth_buttons["sign_out"])
    #     assert homeweb.wait_for_logout()

    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    homeweb_beta.navigate_landing()
    assert homeweb_beta.is_landing()
    lang_prefix = "" if homeweb_beta.language.lower() == "en" else f"/{homeweb_beta.language}"

    resource_1_target = homeweb_beta.base_url + lang_prefix + "/summertime-and-your-health?embedded"
    resource_2_target = homeweb_beta.base_url + lang_prefix + "/mental-health-benefits-of-exercise?embedded"
    resource_3_target = homeweb_beta.base_url + lang_prefix + "/summer-beauty-from-the-inside-out?embedded"

    # 1: Test - Embedded Resource - 1
    homeweb_beta.driver.get(resource_1_target)
    assert homeweb_beta.wait_for_resource_content()
    homeweb_beta.go_back()

    # 2: Test - Embedded Resource - 2
    homeweb_beta.driver.get(resource_2_target)
    assert homeweb_beta.wait_for_resource_content()
    homeweb_beta.go_back()

    # 3: Test - Embedded Resource - 3
    homeweb_beta.driver.get(resource_3_target)
    assert homeweb_beta.wait_for_resource_content()
    homeweb_beta.go_back()

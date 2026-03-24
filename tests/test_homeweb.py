################# BUILD ACCEPTANCE ################
##################### HOMEWEB #####################
from selenium.webdriver.common.by import By


# TODO: Add Pathfinder Assessment

# TEST: Navigate Homeweb
def test_bat_web_001(homeweb):
    # 1: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()
    assert homeweb.domain in homeweb.current_url.lower()


# TEST: Homeweb Landing Articles
def test_bat_web_002(homeweb):
    assert homeweb.is_landing()
    articles = homeweb.get_articles()

    # 1: Test - Resources 1-3 (Dynamic articles -> subject to change)
    for article in articles:
        locator = f'//h3[contains(normalize-space(), "{article["title"]}")]//ancestor::div[contains(@class,"card-container")]//a[@role="button"]'
        homeweb.click_element(By.XPATH, locator)
        assert article["href"] in homeweb.current_url.lower()
        assert homeweb.wait_for_resource_content()
        homeweb.go_back()

    # 2: Test - Resource 4 (Static article)
    resources = homeweb.public["elements"]["resources"]
    paths = homeweb.public["paths"]["resources"]
    homeweb.click_element(By.LINK_TEXT, resources["toolkit"])
    assert paths["toolkit"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()


# TEST: Homeweb Login
def test_bat_web_003(homeweb, quantum, credentials):
    assert homeweb.is_landing()
    buttons = homeweb.public["elements"]["buttons"]

    # 1: Test - Sign In - Button
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - Personal
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert homeweb.wait_for_dashboard()


# TEST: Homeweb Resource
def test_bat_web_004(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = homeweb.base_url + "/" + homeweb.language + "/user/articles/56252b81e40e6f50062aa714"
    homeweb.driver.get(resource_target)
    assert homeweb.wait_for_resource_content()


# TEST: Sentio kick-out
def test_bat_web_005(homeweb):
    assert homeweb.is_authenticated()

    # 1: Navigate to sentio resource
    sentio_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/62c5a1e929ed9c1608d0434b"
    homeweb.driver.get(sentio_resource_target)
    assert homeweb.wait_for_resource_content()

    # 2: Test - Sentio transfer kickout
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_sentio_transfer()
    homeweb.go_back()


# TEST: Homeweb Logout
def test_bat_web_006(homeweb):
    assert homeweb.is_authenticated()
    header = homeweb.header
    header_buttons = header.elements["buttons"]

    # 1: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 2: Test - Logout
    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb.wait_for_logout()
    homeweb.navigate_landing()


# TEST: Homeweb Login - Different user
def test_bat_web_007(homeweb, quantum, credentials):
    assert homeweb.is_landing()
    header = homeweb.header
    header_buttons = header.elements["buttons"]
    paths = header.paths["buttons"]

    # 1: Test - Sign In - Header
    header.click_element(By.CLASS_NAME, header_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - DSG Demo
    quantum.login(credentials["dsg_demo"]["email"], credentials["dsg_demo"]["password"])
    assert homeweb.wait_for_dashboard()


# TEST: Kickouts
def test_bat_web_008(homeweb):
    assert homeweb.is_authenticated()
    childcare_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/579ba4db88db7af01fe6ddd4"
    eldercare_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/579ba49a88db7af01fe6ddc8"
    hra_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/579ba53088db7af01fe6dde6"

    # 1: Test - ChildCare - Lifestage transfer kickout
    homeweb.driver.get(childcare_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()

    # 2: Test - ElderCare - Lifestage transfer kickout
    homeweb.driver.get(eldercare_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()

    # 3: Test - HRA - LifeStyles transfer kickout
    homeweb.driver.get(hra_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestyle_transfer()


# TEST: Course consent
def test_bat_web_009(homeweb):
    assert homeweb.is_authenticated()
    header = homeweb.header
    header_buttons = header.elements["buttons"]

    # 1: Navigate to course
    course_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/564a36083392100756dd3e32"
    homeweb.driver.get(course_target)
    assert homeweb.wait_for_resource_content()

    # 2: Test - Open modal
    homeweb.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"modal\"]")
    assert homeweb.wait_for_modal()

    # 3: Test - Dismiss modal, display course content
    homeweb.click_element(By.CSS_SELECTOR, "[data-bs-dismiss=\"modal\"]")
    # assert homeweb.wait_for_course_content()
    assert homeweb.wait_for_course_content(), "iframe content issue"

    # 4: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 5: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb.wait_for_logout()

    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    homeweb.navigate_landing()


def test_bat_web_010(homeweb, quantum, credentials):
    assert homeweb.is_landing()
    header_anon = homeweb.header
    header_anon_buttons = header_anon.elements["buttons"]
    paths = header_anon.paths["buttons"]

    # 1: Test - Sign In - Header
    header_anon.click_element(By.CLASS_NAME, header_anon_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - HHI Demo
    quantum.login(credentials["hhi_demo"]["email"], credentials["hhi_demo"]["password"])
    assert homeweb.wait_for_dashboard()

    # 3: Test - Check and cancel active appointments
    appointments = homeweb.get_active_appointments()
    topics = [a.topic for a in appointments]

    for topic in topics:
        homeweb.end_services(topic)
        assert homeweb.wait_for_dashboard()
        remaining = homeweb.get_active_appointments()
        assert not any(a.topic == topic for a in remaining)

    # 4: Test - Menu dropdown
    header_auth = homeweb.header
    header_auth_buttons = header_auth.elements["buttons"]
    header_auth.click_element(By.CLASS_NAME, header_auth_buttons["menu"])
    assert header_auth.wait_for_account_menu(), "Menu not found"

    # 5: Test - Logout
    header_auth.click_element(By.CSS_SELECTOR, header_auth_buttons["sign_out"])
    assert homeweb.wait_for_logout()

    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    homeweb.navigate_landing()


# TODO: BAT-WEB-011 | Live Chat
# def test_bat_web_011(homeweb, quantum, credentials):
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
def test_bat_web_012(homeweb):
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
    homeweb.navigate_landing()
    assert homeweb.is_landing()
    lang_prefix = "" if homeweb.language.lower() == "en" else f"/{homeweb.language}"

    resource_1_target = homeweb.base_url + lang_prefix + "/summertime-and-your-health?embedded"
    resource_2_target = homeweb.base_url + lang_prefix + "/mental-health-benefits-of-exercise?embedded"
    resource_3_target = homeweb.base_url + lang_prefix + "/summer-beauty-from-the-inside-out?embedded"

    # 1: Test - Embedded Resource - 1
    homeweb.driver.get(resource_1_target)
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 2: Test - Embedded Resource - 2
    homeweb.driver.get(resource_2_target)
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 3: Test - Embedded Resource - 3
    homeweb.driver.get(resource_3_target)
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

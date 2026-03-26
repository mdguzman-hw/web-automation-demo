# Copyright © 2026 - Homewood Health Inc.

################# BUILD ACCEPTANCE ################
##################### HOMEWEB #####################
import pytest
from selenium.webdriver.common.by import By


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
def test_bat_web_003(homeweb, credentials):
    assert homeweb.is_landing()
    buttons = homeweb.public["elements"]["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Button
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in homeweb.current_url.lower()

    # 2: Test - Login - Homeweb - Personal
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    # quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert homeweb.wait_for_dashboard()


# TEST: Homeweb Resource
def test_bat_web_004(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = homeweb.base_url + "/" + homeweb.language + "/user/articles/56252b81e40e6f50062aa714"
    homeweb.driver.get(resource_target)
    assert homeweb.wait_for_resource_content()


# TODO TEST: Resource Library
# def test_bat_web_005x(homeweb):
#     assert homeweb.is_authenticated()
#
#     # 1: Test - Retrieve Dashboard Tiles
#     # TODO: Investigate if this is expected
#     expected = 6 if homeweb.language == "fr" else 8
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 2: Test - Navigate Resource Library
#     homeweb.click_element(By.LINK_TEXT, dashboard_tiles[2].link_text)
#     assert homeweb.wait_for_resources()
#
#     # 3: Get all primary categories and its subcategories
#     primary_categories = homeweb.get_primary_categories()
#     for category in primary_categories:
#         print(category.text.strip())

# for resource_category in resource_categories:
#     print(resource_category["title"])
#
#     # Click category to expand and get subcategories
#     homeweb.click_element(By.LINK_TEXT, resource_category["title"])
#     assert homeweb.wait_for_resources()
#
#     resource_categories = homeweb.get_primary_categories()
#     active_category = next(c for c in resource_categories if c["title"] == resource_category["title"])
#     print(active_category["subcategories"])
# for resource_category in resource_categories:
#     print(resource_category["title"])
#     print(resource_category["subcategories"])


# TEST: Sentio kickout
def test_bat_web_005(homeweb):
    assert homeweb.is_authenticated()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    # 1: Test - Retrieve Dashboard Tiles
    # TODO: Investigate if this is expected
    expected = 6 if homeweb.language == "fr" else 8
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

    # 2: Test - Navigate Sentio Resource
    sentio_endpoint = "/resources/62c5a1e929ed9c1608d0434b"
    homeweb.click_element(By.LINK_TEXT, dashboard_tiles[1].link_text)
    assert sentio_endpoint in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()

    # 3: Test - Sentio transfer kickout
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


# TEST: Homeweb Login - Different Account
def test_bat_web_007(homeweb, credentials, env):
    if env == "prod":
        email = credentials["dsg_demo"]["email"]
        password = credentials["dsg_demo"]["password"]
    else:
        email = credentials["sentio"]["email"]
        password = credentials["sentio"]["password"]

    assert homeweb.is_landing()
    header = homeweb.header
    header_buttons = header.elements["buttons"]
    paths = header.paths["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Header
    header.click_element(By.CLASS_NAME, header_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - DSG Demo
    quantum.login(email, password)
    assert homeweb.wait_for_dashboard()


# TEST: Kickouts
def test_bat_web_008(homeweb):
    childcare_endpoint = "/resources/579ba4db88db7af01fe6ddd4"
    eldercare_endpoint = "/resources/579ba49a88db7af01fe6ddc8"
    hra_endpoint = "/resources/579ba53088db7af01fe6dde6"

    assert homeweb.is_authenticated()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    # 1: Test - Retrieve Dashboard Tiles
    # TODO: Investigate if this is expected
    expected = 6 if homeweb.language == "fr" else 8
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

    # 2: Test: Childcare Resource Locator
    childcare_tile = next(t for t in dashboard_tiles if childcare_endpoint in t.href)
    childcare_tile.click()
    assert childcare_endpoint in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()
    homeweb.navigate_landing()
    assert homeweb.domain in homeweb.current_url.lower()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

    # 3: Test: Eldercare Resource Locator
    eldercare_tile = next(t for t in dashboard_tiles if eldercare_endpoint in t.href)
    eldercare_tile.click()
    assert eldercare_endpoint in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()
    homeweb.navigate_landing()
    assert homeweb.domain in homeweb.current_url.lower()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

    # 4: Test: Health Risk Assessment
    hra_tile = next(t for t in dashboard_tiles if hra_endpoint in t.href)
    hra_tile.click()
    assert hra_endpoint in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestyle_transfer()
    homeweb.navigate_landing()
    assert homeweb.domain in homeweb.current_url.lower()


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
    assert homeweb.wait_for_course_content()

    # 4: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu()

    # 5: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb.wait_for_logout()

    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    homeweb.navigate_landing()


# TEST: DEMO - Cancel Active Services
def test_bat_web_010(homeweb, quantum, credentials, env):
    if env == "beta":
        return pytest.skip(f"Skipping {env} test_bat_web_010")

    assert homeweb.is_landing()
    header_anon = homeweb.header
    header_anon_buttons = header_anon.elements["buttons"]
    paths = header_anon.paths["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Header
    header_anon.click_element(By.CLASS_NAME, header_anon_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - HHI Demo

    quantum.login(credentials["hhi_demo"]["email"], credentials["hhi_demo"]["password"])
    assert homeweb.wait_for_dashboard()

    # 3: Test - Check and cancel active appointments
    appointments = homeweb.get_active_services()
    topics = [a.topic for a in appointments]

    for topic in topics:
        homeweb.end_services(topic)
        assert homeweb.wait_for_dashboard()
        remaining = homeweb.get_active_services()
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


# TEST: Live Chat
def test_bat_web_011(homeweb, quantum, credentials, env):
    # Manual for now
    pytest.skip(f"Skipping Live Chat {env} test_bat_web_011")

    homeweb.navigate_landing()
    assert homeweb.domain in homeweb.current_url.lower()
    header_anon = homeweb.header
    header_anon_buttons = header_anon.elements["buttons"]
    paths = header_anon.paths["buttons"]

    # 1: Test - Sign In - Header
    header_anon.click_element(By.CLASS_NAME, header_anon_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - DSG Demo
    email = credentials["sentio"]["email"]
    quantum.login(email, credentials["sentio"]["password"])
    assert homeweb.wait_for_dashboard()

    homeweb.test_live_chat(email)


# TEST: Complete Pathfinder Assessment
def test_bat_web_012(homeweb, credentials):
    assert homeweb.is_landing()
    header_anon = homeweb.header
    header_anon_buttons = header_anon.elements["buttons"]
    paths = header_anon.paths["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Header
    header_anon.click_element(By.CLASS_NAME, header_anon_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - DSG Demo
    quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert homeweb.wait_for_dashboard()

    # 3: Test - Check and cancel active services
    appointments = homeweb.get_active_services()
    topics = [a.topic for a in appointments]

    for topic in topics:
        homeweb.end_services(topic)
        assert homeweb.wait_for_dashboard()
        remaining = homeweb.get_active_services()
        assert not any(a.topic == topic for a in remaining)

    # TODO: Investigate if this is expected
    # 4: Test - Retrieve Dashboard Tiles
    expected = 6 if homeweb.language == "fr" else 8
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

    # 5: Test - Navigate Assessment
    homeweb.click_element(By.LINK_TEXT, dashboard_tiles[0].link_text)
    assessment_endpoint = "pathfinder/assessment"
    assert assessment_endpoint in homeweb.current_url
    assert homeweb.wait_for_assessment()

    # 6: Test - Complete Assessment
    # TODO: Support passing in answers as parameter, to go through specific pathfinder flows
    homeweb.complete_assessment(
        # answers={
        #     0: "Work & career",
        #     1: "Work stress"
        # }
    )
    assert homeweb.is_assessment_complete()


# TEST: Create Pathfinder Booking
def test_bat_web_013(homeweb, credentials):
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()
    email = credentials["sentio"]["email"]

    homeweb.navigate_recommendations()
    assert homeweb.wait_for_recommendation()

    homeweb.navigate_rating()
    assert homeweb.wait_for_rating()

    homeweb.complete_rating()
    assert homeweb.wait_for_booking_create()

    homeweb.complete_booking_create_form()
    assert homeweb.wait_for_service_confirm()

    homeweb.complete_service_confirm_form(email)
    assert homeweb.wait_for_booking_digest()


# TODO: TEST: Complete Pathfinder Booking
def test_bat_web_014(homeweb, credentials):
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    # 1: Test - Check Active Services
    appointments = homeweb.get_active_services()
    topics = [a.topic for a in appointments]
    print(topics)

    homeweb.continue_booking(topics[0])
    assert homeweb.wait_for_booking_digest()

    homeweb.select_provider()
    assert homeweb.wait_for_booking_details()

    homeweb.select_booking_options()
    assert homeweb.wait_for_booking_confirm()

    homeweb.confirm_booking()
    # TODO: Assert Continue to Booking button is no longer visible
    # Booking Confirmed - Sufficient for now. See Additional Tests Below

    # Additional Tests
    # TEST: Confirmation Method
    homeweb.choose_confirmation_method()
    # : Test - Menu dropdown
    header_auth = homeweb.header
    header_auth_buttons = header_auth.elements["buttons"]
    header_auth.click_element(By.CLASS_NAME, header_auth_buttons["menu"])
    assert header_auth.wait_for_account_menu(), "Menu not found"

    # : Test - Logout
    header_auth.click_element(By.CSS_SELECTOR, header_auth_buttons["sign_out"])
    assert homeweb.wait_for_logout()


# TEST: Mobile - Embedded resources
def test_bat_web_015(homeweb):
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

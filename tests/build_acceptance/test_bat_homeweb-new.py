# Copyright © 2026 - Homewood Health Inc.

################# BUILD ACCEPTANCE ################
##################### HOMEWEB #####################
################# NEW PORTAL - BETA ###############
import pytest
from selenium.webdriver.common.by import By

# CORE MODULES
# Registration
# Login
# Dashboard - S1
# Dashboard - S2
# Dashboard - S3
# Discover - Mental Health
# Discover - Wellness
# Discover - Work-Life
# Journey - Plans
# Journey - Sessions
# Journey - Appointments
# Smart Care Navigation
# Booking
# Profile
# Library
# Messages

# BAT-WEB-001 | Navigate Homeweb
def test_bat_web_001(homeweb, quantum, env, record_version):
    # 1: Test - Check versions
    suffix = " - Beta" if env == "beta" else ""
    record_version(f"Homeweb{suffix}", homeweb.base_url, env)
    record_version(f"Quantum API{suffix}", quantum.base_url, env)

    # 2: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()
    assert homeweb.domain in homeweb.current_url.lower(), \
        f"EXPECTED: '{homeweb.domain}' | ACTUAL: {homeweb.current_url}"


# BAT-WEB-002 | Homeweb Landing Articles
def test_bat_web_002(homeweb):
    assert homeweb.is_landing(), "NOT ON LANDING PAGE"
    articles = homeweb.get_articles()

    # 1: Test - Resources 1-3 (Dynamic articles -> subject to change)
    for article in articles:
        locator = f'//h3[contains(normalize-space(), "{article["title"]}")]//ancestor::div[contains(@class,"card-container")]//a[@role="button"]'
        homeweb.click_element(By.XPATH, locator)
        assert article["href"] in homeweb.current_url.lower(), \
            f"EXPECTED: '{article['href']}' | ACTUAL: {homeweb.current_url}"
        assert homeweb.wait_for_resource_content(), \
            f"Resource content did not load for article: '{article['title']}'"
        homeweb.go_back()

    # 2: Test - Resource 4 (Static article)
    resources = homeweb.public["elements"]["resources"]
    paths = homeweb.public["paths"]["resources"]
    homeweb.click_element(By.LINK_TEXT, resources["toolkit"])
    assert paths["toolkit"] in homeweb.current_url.lower(), \
        f"Expected toolkit path '{paths['toolkit']}' in URL, got: {homeweb.current_url}"
    assert homeweb.wait_for_resource_content(), "Toolkit resource content did not load"
    homeweb.go_back()


# BAT-WEB-003 | Homeweb Login
def test_bat_web_003(homeweb, credentials):
    assert homeweb.is_landing(), "Expected to be on landing page before login"
    buttons = homeweb.public["elements"]["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Button
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in homeweb.current_url.lower(), \
        f"Expected Quantum domain '{quantum.domain}' in URL after Sign In, got: {homeweb.current_url}"

    # 2: Test - Login - Homeweb - Fresh 1
    quantum.login(credentials["fresh_1"]["email"], credentials["fresh_1"]["password"])
    assert homeweb.wait_for_dashboard(), \
        f"Dashboard did not load after login for '{credentials['fresh_1']['email']}'"


# # BAT-WEB-004 | Homeweb Resource
def test_bat_web_004(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = homeweb.base_url + "/" + homeweb.language + "/user/articles/56252b81e40e6f50062aa714"
    homeweb.driver.get(resource_target)
    assert homeweb.wait_for_resource_content()


# # BAT-WEB-005 | Sentio Kickout
# def test_bat_web_005(homeweb):
#     assert homeweb.is_authenticated()
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#
#     # 1: Test - Retrieve Dashboard Tiles
#     # TODO: Verify tile count on new portal (was 6 FR / 8 EN on old portal)
#     expected = 6 if homeweb.language == "fr" else 8
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 2: Test - Navigate Sentio Resource
#     sentio_endpoint = "/resources/62c5a1e929ed9c1608d0434b"
#     homeweb.click_element(By.LINK_TEXT, dashboard_tiles[1].link_text)
#     assert sentio_endpoint in homeweb.current_url.lower()
#     assert homeweb.wait_for_resource_content()
#
#     # 3: Test - Sentio transfer kickout
#     homeweb.click_element(By.CLASS_NAME, "btn-primary")
#     assert homeweb.wait_for_sentio_transfer()
#     homeweb.go_back()
#
#
# # BAT-WEB-006 | Complete Pathfinder Assessment - Scenario 4
# # Employee at Homewood Health Inc (HHI Employee Program)
# # Resource ONLY
# def test_bat_web_006(homeweb, record_output):
#     assert homeweb.is_authenticated()
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#
#     # 1: Test - Retrieve Dashboard Tiles
#     # TODO: Verify tile count on new portal (was 6 FR / 8 EN on old portal)
#     expected = 6 if homeweb.language == "fr" else 8
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 2: Test - Navigate Assessment
#     homeweb.click_element(By.LINK_TEXT, dashboard_tiles[0].link_text)
#     assessment_endpoint = "pathfinder/assessment"
#     assert assessment_endpoint in homeweb.current_url
#     assert homeweb.wait_for_assessment()
#
#     # 3: Test - Complete Assessment
#     homeweb.complete_assessment(logger=record_output)
#     assert homeweb.is_assessment_complete()
#     homeweb.assert_recommendation_scenario_4()
#
#
# # BAT-WEB-007 | Homeweb Logout
# def test_bat_web_007(homeweb):
#     assert homeweb.is_authenticated()
#     header = homeweb.header
#     header_buttons = header.elements["buttons"]
#
#     # 1: Test - Menu dropdown
#     header.click_element(By.CLASS_NAME, header_buttons["menu"])
#     assert header.wait_for_account_menu(), "Menu not found"
#
#     # 2: Test - Logout
#     # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
#     header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
#     assert homeweb.wait_for_logout()
#     homeweb.navigate_landing()
#
#
# # BAT-WEB-008 | Homeweb Login - Different Account
# def test_bat_web_008(homeweb, credentials, env):
#     # Fresh 2 used for all environments on the new portal
#     email = credentials["fresh_2"]["email"]
#     password = credentials["fresh_2"]["password"]
#
#     assert homeweb.is_landing()
#     header = homeweb.header
#     header_buttons = header.elements["buttons"]
#     paths = header.paths["buttons"]
#     quantum = homeweb.quantum
#
#     # 1: Test - Sign In - Header
#     header.click_element(By.CLASS_NAME, header_buttons["sign_in"])
#     assert paths["sign_in"] in quantum.current_url.lower()
#
#     # 2: Test - Login - Homeweb - Fresh 2
#     quantum.login(email, password)
#     assert homeweb.wait_for_dashboard()
#
#
# # BAT-WEB-009 | Kickouts
# def test_bat_web_009(homeweb, env):
#     if env == "beta":
#         return pytest.skip(f"Skipping {env}. KNOWN ISSUE")
#
#     childcare_endpoint = "/resources/579ba4db88db7af01fe6ddd4"
#     eldercare_endpoint = "/resources/579ba49a88db7af01fe6ddc8"
#     hra_endpoint = "/resources/579ba53088db7af01fe6dde6"
#
#     assert homeweb.is_authenticated()
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#
#     # 1: Test - Retrieve Dashboard Tiles
#     # TODO: Verify tile count on new portal (was 6 FR / 8 EN on old portal)
#     expected = 6 if homeweb.language == "fr" else 8
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 2: Test: Childcare Resource Locator
#     childcare_tile = dashboard_tiles[4]
#     childcare_tile.navigate()
#     assert childcare_endpoint in homeweb.current_url.lower()
#     assert homeweb.wait_for_resource_content()
#     homeweb.click_element(By.CLASS_NAME, "btn-primary")
#     assert homeweb.wait_for_lifestage_transfer()
#
#     homeweb.navigate_landing()
#     assert homeweb.domain in homeweb.current_url.lower()
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 3: Test: Eldercare Resource Locator
#     eldercare_tile = dashboard_tiles[5]
#     eldercare_tile.navigate()
#     assert eldercare_endpoint in homeweb.current_url.lower()
#     assert homeweb.wait_for_resource_content()
#     homeweb.click_element(By.CLASS_NAME, "btn-primary")
#     assert homeweb.wait_for_lifestage_transfer()
#
#     homeweb.navigate_landing()
#     assert homeweb.domain in homeweb.current_url.lower()
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 4: Test: Health Risk Assessment
#     hra_tile = dashboard_tiles[7]
#     hra_tile.navigate()
#     assert hra_endpoint in homeweb.current_url.lower()
#     assert homeweb.wait_for_resource_content()
#     homeweb.click_element(By.CLASS_NAME, "btn-primary")
#     assert homeweb.wait_for_lifestyle_transfer()
#     homeweb.navigate_landing()
#     assert homeweb.domain in homeweb.current_url.lower()
#
#
# # BAT-WEB-010 | Course Consent
# def test_bat_web_010(homeweb):
#     assert homeweb.is_authenticated()
#     header = homeweb.header
#     header_buttons = header.elements["buttons"]
#
#     # 1: Navigate to course
#     course_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/564a36083392100756dd3e32"
#     homeweb.driver.get(course_target)
#     assert homeweb.wait_for_resource_content()
#
#     # 2: Test - Open modal
#     homeweb.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"modal\"]")
#     assert homeweb.wait_for_modal()
#
#     # 3: Test - Dismiss modal, display course content
#     homeweb.click_element(By.CSS_SELECTOR, "[data-bs-dismiss=\"modal\"]")
#     assert homeweb.wait_for_course_content()
#
#     # 4: Test - Menu dropdown
#     header.click_element(By.CLASS_NAME, header_buttons["menu"])
#     assert header.wait_for_account_menu()
#
#     # 5: Test - Logout
#     header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
#     assert homeweb.wait_for_logout()
#
#     # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
#     homeweb.navigate_landing()
#
#
# # BAT-WEB-011 | Cancel Active Services
# # [SKIP - WIP]
# def test_bat_web_011(homeweb, quantum, credentials, env):
#     pytest.skip("Skipping Cancel Active Services -> WIP")
#
#
# # BAT-WEB-012 | Live Chat
# # [SKIP - MANUAL]
# def test_bat_web_012(homeweb, quantum, credentials, env):
#     pytest.skip("Skipping Live Chat -> MANUAL TEST")
#
#
# # BAT-WEB-013 | Complete Pathfinder Assessment - Scenario 1
# # Mental Health > Anxiety > High Severity > Low Risk
# # Professional Support & Sentio iCBT
# def test_bat_web_013(homeweb, credentials, record_output):
#     assert homeweb.is_landing()
#     header_anon = homeweb.header
#     header_anon_buttons = header_anon.elements["buttons"]
#     paths = header_anon.paths["buttons"]
#     quantum = homeweb.quantum
#
#     # 1: Test - Sign In - Header
#     header_anon.click_element(By.CLASS_NAME, header_anon_buttons["sign_in"])
#     assert paths["sign_in"] in quantum.current_url.lower()
#
#     # 2: Test - Login - Homeweb - Fresh 2
#     quantum.login(credentials["fresh_2"]["email"], credentials["fresh_2"]["password"])
#     assert homeweb.wait_for_dashboard()
#
#     # 3: Test - Check and cancel active services
#     appointments = homeweb.get_active_services()
#     topics = [a.topic for a in appointments]
#
#     for topic in topics:
#         homeweb.end_services(topic)
#         assert homeweb.wait_for_dashboard()
#         remaining = homeweb.get_active_services()
#         assert not any(a.topic == topic for a in remaining)
#
#     pytest.skip("Skipping Scenario 1. MANUAL TEST")
#
#     # 4: Test - Retrieve Dashboard Tiles
#     expected = 6 if homeweb.language == "fr" else 8
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 5: Test - Navigate Assessment
#     homeweb.click_element(By.LINK_TEXT, dashboard_tiles[0].link_text)
#     assessment_endpoint = "pathfinder/assessment"
#     assert assessment_endpoint in homeweb.current_url
#     assert homeweb.wait_for_assessment()
#
#     # 6: Test - Complete Assessment
#     flow = [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
#     homeweb.complete_assessment(flow, logger=record_output)
#     assert homeweb.is_assessment_complete()
#     homeweb.assert_recommendation_scenario_1()
#
#
# # BAT-WEB-014 | Complete Pathfinder Assessment - Scenario 2
# # Mental Health > Anxiety > Low Severity > Low Risk
# # Sentio iCBT ONLY
# # [SKIP - MANUAL]
# def test_bat_web_014(homeweb, credentials, record_output):
#     pytest.skip("Skipping Scenario 2 -> MANUAL TEST")
#
#
# # BAT-WEB-015 | Complete Pathfinder Assessment - Scenario 3
# # Work & Career > Anger > Low Severity > Low Risk
# # Professional Support ONLY
# def test_bat_web_015(homeweb, credentials, record_output):
#     assert homeweb.is_authenticated()
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#
#     # 1: Test - Retrieve Dashboard Tiles
#     # TODO: Verify tile count on new portal (was 6 FR / 8 EN on old portal)
#     expected = 6 if homeweb.language == "fr" else 8
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 2: Test - Navigate Assessment
#     homeweb.click_element(By.LINK_TEXT, dashboard_tiles[0].link_text)
#     assessment_endpoint = "pathfinder/assessment"
#     assert assessment_endpoint in homeweb.current_url
#     assert homeweb.wait_for_assessment()
#
#     # 3: Test - Complete Assessment
#     flow = [2, 1, 1]
#     homeweb.complete_assessment(flow, logger=record_output)
#     assert homeweb.is_assessment_complete()
#     homeweb.assert_recommendation_scenario_3()
#
#
# # BAT-WEB-016 | Create Pathfinder Booking
# # [SKIP - WIP]
# def test_bat_web_016(homeweb, credentials, env):
#     pytest.skip("Skipping Create Booking -> WIP")
#
#
# # BAT-WEB-017 | Complete Pathfinder Booking
# # [SKIP - WIP]
# def test_bat_web_017(homeweb, credentials):
#     pytest.skip("Skipping Complete Booking -> WIP")
#
#
# # BAT-WEB-018 | Complete Pathfinder Assessment - Scenario 5
# # Legal flow
# # Financial flow
# def test_bat_web_018(homeweb, credentials, record_output):
#     assert homeweb.is_authenticated()
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#
#     # 1: Test - Retrieve Dashboard Tiles
#     # TODO: Verify tile count on new portal (was 6 FR / 8 EN on old portal)
#     expected = 6 if homeweb.language == "fr" else 8
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 2: Test - Navigate Assessment - Legal > Real estate law
#     homeweb.click_element(By.LINK_TEXT, dashboard_tiles[0].link_text)
#     assessment_endpoint = "pathfinder/assessment"
#     assert assessment_endpoint in homeweb.current_url
#     assert homeweb.wait_for_assessment()
#
#     # 3: Test - Complete Assessment - Legal > Real estate law
#     flow = [3, 3]
#     homeweb.complete_assessment(flow, logger=record_output)
#     assert homeweb.is_assessment_complete()
#     homeweb.assert_recommendation_scenario_3()
#
#     homeweb.navigate_dashboard()
#     assert homeweb.wait_for_dashboard()
#
#     # 4: Test - Retrieve Dashboard Tiles
#     dashboard_tiles = homeweb.get_dashboard_tiles()
#     assert len(dashboard_tiles) == expected
#
#     # 5: Test - Navigate Assessment - Financial > Bankruptcy
#     homeweb.click_element(By.LINK_TEXT, dashboard_tiles[0].link_text)
#     assert assessment_endpoint in homeweb.current_url
#     assert homeweb.wait_for_assessment()
#
#     # 6: Test - Complete Assessment - Financial > Bankruptcy
#     flow = [4, 4]
#     homeweb.complete_assessment(flow, logger=record_output)
#     assert homeweb.is_assessment_complete()
#     homeweb.assert_recommendation_scenario_3()
#
#
# # BAT-WEB-019 | Resource Library
# def test_bat_web_019(homeweb):
#     assert homeweb.is_authenticated()
#
#     # 1: Test - Navigate to Resources
#     homeweb.navigate_resources()
#     assert homeweb.wait_for_resources()
#
#     # 2: Test - Primary categories are visible
#     categories = homeweb.get_resource_categories()
#     assert len(categories) > 0
#
#
# # BAT-WEB-020 | Primary Category
# def test_bat_web_020(homeweb, record_output):
#     assert homeweb.wait_for_resources()
#
#     # 1: Test - Click first primary category
#     categories = homeweb.get_resource_categories()
#     first_category = categories[0]
#     category_name = first_category.text.strip()
#     record_output(f"Category: {category_name}")
#     first_category.click()
#
#     # 2: Test - Category page loaded
#     assert homeweb.wait_for_resources()
#
#
# # BAT-WEB-021 | Subcategory
# def test_bat_web_021(homeweb, record_output):
#     assert homeweb.wait_for_resources()
#
#     # 1: Test - Get subcategories from active primary category
#     subcategories = homeweb.get_resource_subcategories()
#     assert len(subcategories) > 0
#
#     # 2: Test - Click first subcategory
#     first_subcategory = subcategories[0]
#     subcategory_name = first_subcategory.text.strip()
#     record_output(f"Subcategory: {subcategory_name}")
#     first_subcategory.click()
#
#     # 3: Test - Subcategory page loaded
#     assert homeweb.wait_for_resources()
#
#
# # BAT-WEB-022 | Search
# def test_bat_web_022(homeweb):
#     assert homeweb.is_authenticated()
#
#     # 1: Test - Navigate to resources
#     homeweb.navigate_resources()
#     assert homeweb.wait_for_resources()
#
#     # 2: Test - Perform search
#     homeweb.search_resources("mental health")
#     assert homeweb.wait_for_search_results()
#
#     # 3: Test - Logout
#     header_auth = homeweb.header
#     header_auth_buttons = header_auth.elements["buttons"]
#     header_auth.click_element(By.CLASS_NAME, header_auth_buttons["menu"])
#     assert header_auth.wait_for_account_menu(), "Menu not found"
#     header_auth.click_element(By.CSS_SELECTOR, header_auth_buttons["sign_out"])
#     assert homeweb.wait_for_logout()
#
# # BAT-WEB-023 | Embedded Resources
# def test_bat_web_023(homeweb):
#     # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
#     homeweb.navigate_landing()
#     assert homeweb.is_landing()
#     lang_prefix = "" if homeweb.language.lower() == "en" else f"/{homeweb.language}"
#
#     resource_1_target = homeweb.base_url + lang_prefix + "/summertime-and-your-health?embedded"
#     resource_2_target = homeweb.base_url + lang_prefix + "/mental-health-benefits-of-exercise?embedded"
#     resource_3_target = homeweb.base_url + lang_prefix + "/summer-beauty-from-the-inside-out?embedded"
#
#     # 1: Test - Embedded Resource - 1
#     homeweb.driver.get(resource_1_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.go_back()
#
#     # 2: Test - Embedded Resource - 2
#     homeweb.driver.get(resource_2_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.go_back()
#
#     # 3: Test - Embedded Resource - 3
#     homeweb.driver.get(resource_3_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.go_back()
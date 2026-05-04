# Copyright © 2026 - Homewood Health Inc.

################# BUILD ACCEPTANCE ################
##################### HOMEWEB #####################
################# NEW PORTAL - BETA ###############
from datetime import datetime

import pytest
from selenium.webdriver.common.by import By


# CORE MODULES
# [HOLD] - Registration
# [DONE] Standard | DSGDEMO
# [HOLD] MFA | Canada Post Corporation
# [HOLD] Custom | LSO, Alumni, Equitable
# [HOLD] Eligibility List | Canada Post Corporation
# [HOLD] Additional Fields | Alumni, Equitable, etc.
# [HOLD] Registration/Invitation Code | Dependents invite?? PAC?

# [HOLD] Login
# [DONE] - DSGDEMO
# [DONE] - HHI

# [NEXT] Dashboard - S1
# TODO - Onboarding

# [NEXT] Dashboard - S2

# [NEXT] Dashboard - S3

# [NEXT] Discover - Mental Health
# [NEXT] Discover - Wellness
# [NEXT] Discover - Work-Life

# [NEXT] Journey - Plans
# [NEXT] Journey - Sessions
# [NEXT] Journey - Appointments

# [WIP] Smart Care Navigation
# [DONE] - Scenario 1: Resource ONLY
# [DONE] - Scenario 2: Professional Support & Sentio
# [DONE] - Scenario 3: Professional Support ONLY
# [WIP] - Scenario 4: Sentio ONLY
# [WIP] - Scenario 5: Legal Flow
# [WIP] - Scenario 6: Financial Flow

# [NEXT] Booking
# [NEXT] Profile

# Library
# [DONE] - Resource Library
# [DONE] - Primary Category
# [DONE] - Subcategory

# [DONE] Messages


# BAT-WEB-001 | Navigate Homeweb
def test_bat_web_001(homeweb, quantum, env, record_version):
    # 1: Test - Check versions
    suffix = " - Beta" if env == "beta" else ""
    record_version(f"Homeweb{suffix}", homeweb.base_url, env)
    record_version(f"Quantum API{suffix}", quantum.base_url, env)

    # 2: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()


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
            f"RESOURCE NOT LOADED: '{article['title']}'"
        homeweb.go_back()

    # 2: Test - Resource 4 (Static article)
    resources = homeweb.public["elements"]["resources"]
    paths = homeweb.public["paths"]["resources"]
    homeweb.click_element(By.LINK_TEXT, resources["toolkit"])
    assert paths["toolkit"] in homeweb.current_url.lower(), \
        f"EXPECTED: '{paths['toolkit']}' | ACTUAL: {homeweb.current_url}"
    assert homeweb.wait_for_resource_content(), "TOOLKIT NOT LOADED"
    homeweb.go_back()


# BAT-WEB-003 | Standard Registration - Organization: DSGDEMO
# Step 2 is skipped - No division
def test_bat_web_003(homeweb, credentials, env, record_output, record_account):
    # TODO: UNDO
    pytest.skip("TEMP. Do not forget to UNDO!")

    assert homeweb.is_landing(), "NOT ON LANDING PAGE"
    buttons = homeweb.public["elements"]["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Navigate to Quantum API Gateway
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in homeweb.current_url.lower(), \
        f"EXPECTED: '{quantum.domain}' | ACTUAL: {homeweb.current_url}"

    # 2: Test - Navigate to Register
    sign_up_text = "Sign up" if homeweb.language == "en" else "S'inscrire"
    quantum.click_element(By.LINK_TEXT, sign_up_text)
    assert "register" in quantum.current_url.lower(), \
        f"EXPECTED: 'register' | ACTUAL: {quantum.current_url}"
    # registration_code = re.search(r"register/([^/]+)", quantum.current_url)
    # registration_code = registration_code.group(1) if registration_code else "N/A"

    # 3: Registration - Step 1 | Organization
    record_output("Standard Registration")
    assert quantum.wait_for_org_search()
    quantum.search_org("DSG")
    assert quantum.wait_for_org_results()
    quantum.select_org("DSGDEMO")
    record_output("Step 1 | Organization: DSGDEMO")
    assert quantum.wait_for_url_path("/role"), \
        f"EXPECTED: '/role' in URL | ACTUAL: {quantum.current_url}"

    record_output("Step 2 | Division: N/A ")

    # 4: Registration - Step 3 | Role
    assert quantum.wait_for_role_selection()
    quantum.select_role("ROLE_USER")
    quantum.continue_registration()
    record_output("Step 3 | Role: Employee")
    assert quantum.wait_for_url_path("/details"), \
        f"EXPECTED: '/details' in URL | ACTUAL: {quantum.current_url}"

    # 5: Registration - Step 4 | Details
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    first_name = f"Automation-{timestamp}"
    last_name = "DSGDEMO-Employee"
    preferred_name = f"{timestamp}-Automation"
    email = f"dsgdemo-employee-automation-{timestamp}@demo.com"
    dob = "2000-01-01"

    assert quantum.wait_for_registration_details()
    quantum.fill_registration_details(first_name, last_name, preferred_name, email, dob)
    quantum.continue_registration()
    record_output(f"Step 4 | Name: {first_name} {last_name} | Email: {email} | DOB: {dob}")
    assert quantum.wait_for_url_path("/verify"), \
        f"EXPECTED: '/verify' in URL | ACTUAL: {quantum.current_url}"

    # 6: Registration - Step 5 | Verify Email
    # TODO: Wire in directly with email (retrieve code via email API/IMAP)
    verification_code = input("Step 5 | Enter 6-digit verification code: ")
    quantum.enter_email_verification_code(verification_code)
    record_output(f"Step 5 | Verification code entered")
    quantum.continue_from_verify()
    assert quantum.wait_for_url_path("/password"), \
        f"EXPECTED: '/password' in URL | ACTUAL: {quantum.current_url}"

    # 7: Registration - Step 6 | Password
    password = "QuantumSentio123$"
    quantum.fill_password_form(password, marketing_opt_in=False)
    record_output(f"Step 6 | Password: {password} | Marketing opt-in: Off")

    assert quantum.wait_for_url_path("/login"), \
        f"EXPECTED: '/login' in URL | ACTUAL: {quantum.current_url}"
    assert quantum.domain in quantum.current_url.lower(), \
        f"EXPECTED: '{quantum.domain}' | ACTUAL: {quantum.current_url}"

    record_account(env, "DSGDEMO", "N/A", "Employee", first_name, last_name, preferred_name, email, dob, password, False)
    record_output("Account successfully created.")


# BAT-WEB-004 | Homeweb Login
def test_bat_web_004(homeweb, quantum, latest_registered_account, record_output):
    # TODO: UNDO
    # assert quantum.domain in quantum.current_url.lower(), \
    #     f"EXPECTED: '{quantum.domain}' | ACTUAL: {quantum.current_url}"

    # TODO: UNDO, just by passing registration
    assert homeweb.is_landing()
    buttons = homeweb.public["elements"]["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Button
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in homeweb.current_url.lower()

    # 2: Test - Login with latest registered account
    email = latest_registered_account["Email"]
    password = latest_registered_account["Password"]
    quantum.login(email, password)
    record_output(f"Login | Email: {email}")
    assert homeweb.wait_for_dashboard(), \
        f"DASHBOARD NOT LOADED: '{homeweb.current_url}'"


# BAT-WEB-005 | Homeweb Resource
def test_bat_web_005(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = homeweb.base_url + "/" + homeweb.language + "/user/articles/56252b81e40e6f50062aa714"
    homeweb.driver.get(resource_target)
    assert homeweb.wait_for_resource_content(), \
        f"RESOURCE NOT LOADED"


# BAT-WEB-006 | Resource Library
def test_bat_web_006(homeweb, record_output):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to Resources
    homeweb.navigate_library()
    assert homeweb.wait_for_resources()

    # 2: Test - Primary categories are visible
    categories = homeweb.get_resource_categories()
    assert len(categories) > 0
    category_names = [c.text.strip() for c in categories]
    record_output(f"Resource categories ({len(category_names)}): {', '.join(category_names)}")


# BAT-WEB-007 | Primary Category
def test_bat_web_007(homeweb, record_output):
    assert homeweb.wait_for_resources()

    # 1: Test - Click first primary category
    categories = homeweb.get_resource_categories()
    first_category = categories[0]
    category_name = first_category.text.strip()
    record_output(f"Category: {category_name}")
    first_category.click()

    # 2: Test - Category page loaded
    assert homeweb.wait_for_resources()


# BAT-WEB-008 | Subcategory
def test_bat_web_008(homeweb, record_output):
    assert homeweb.wait_for_resources()

    # 1: Test - Get subcategories from active primary category
    subcategories = homeweb.get_resource_subcategories()
    assert len(subcategories) > 0

    # 2: Test - Click first subcategory
    first_subcategory = subcategories[0]
    subcategory_name = first_subcategory.text.strip()
    record_output(f"Subcategory: {subcategory_name}")
    first_subcategory.click()

    # 3: Test - Subcategory page loaded
    assert homeweb.wait_for_resources()


# BAT-WEB-009 | Search
def test_bat_web_009(homeweb):
    assert homeweb.wait_for_resources()

    # 1: Test - Perform search
    homeweb.search_resources("mental health")
    assert homeweb.wait_for_search_results()


# BAT-WEB-010 | Kickouts
def test_bat_web_010(homeweb, env, record_output):
    pytest.skip("Skipping -> HRA kickout | KNOWN ISSUE")
    assert homeweb.wait_for_resources()

    is_fr = homeweb.language == "fr"
    resources_to_find = [
        ("Localisateur de ressources pour les soins aux enfants – Soutien Étapes-vie" if is_fr else "Childcare Resource Locator by LifestageCare", "/resources/579ba4db88db7af01fe6ddd4", "lifestage"),
        ("Localisateur de ressources pour les soins aux aînés – Soutien Étapes-vie" if is_fr else "Eldercare Resource Locator by LifestageCare", "/resources/579ba49a88db7af01fe6ddc8", "lifestage"),
        ("Le Questionnaire santé" if is_fr else "Health Risk Assessment", "/resources/579ba53088db7af01fe6dde6", "lifestyle"),
    ]

    for search_term, endpoint, transfer_type in resources_to_find:
        homeweb.search_and_open_resource(search_term)
        assert homeweb.wait_for_resource_content(), f"RESOURCE NOT LOADED: '{search_term}'"
        assert endpoint in homeweb.current_url.lower(), \
            f"EXPECTED: '{endpoint}' | ACTUAL: {homeweb.current_url}"

        homeweb.click_element(By.CLASS_NAME, "btn-primary")
        homeweb.handle_transfer_consent()
        if transfer_type == "lifestage":
            assert homeweb.wait_for_lifestage_transfer(), f"LIFESTAGE TRANSFER FAILED: '{search_term}'"
        else:
            # KNOWN ISSUE
            assert homeweb.wait_for_lifestyle_transfer(), f"LIFESTYLE TRANSFER FAILED: '{search_term}'"

        record_output(f"Kickout | '{search_term}' | {transfer_type} transfer confirmed")
        homeweb.navigate_landing()
        assert homeweb.domain in homeweb.current_url.lower()
        homeweb.navigate_library()
        assert homeweb.wait_for_resources()


# BAT-WEB-011 | Sentio Kickout
def test_bat_web_011(homeweb, record_output):
    sentio_endpoint = "/resources/62c5a1e929ed9c1608d0434b"
    search_term = "Sentio par Homewood Santé" if homeweb.language == "fr" else "Sentio by Homewood Health"

    assert homeweb.wait_for_resources()

    # 1: Test - Search and navigate to Sentio resource
    homeweb.search_and_open_resource(search_term)
    assert homeweb.wait_for_resource_content(), f"RESOURCE NOT LOADED: '{search_term}'"
    assert sentio_endpoint in homeweb.current_url.lower(), \
        f"EXPECTED: '{sentio_endpoint}' | ACTUAL: {homeweb.current_url}"
    record_output(f"Sentio resource loaded | {sentio_endpoint}")

    # 3: Test - Sentio transfer kickout
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    homeweb.handle_transfer_consent()
    assert homeweb.wait_for_sentio_transfer(), "SENTIO TRANSFER FAILED"
    record_output("Sentio kickout confirmed")
    homeweb.go_back()


# BAT-WEB-012 | Course Consent
def test_bat_web_012(homeweb, record_output):
    homeweb.navigate_library()
    assert homeweb.wait_for_resources()
    course_endpoint = "/resources/564a36083392100756dd3e32"
    search_term = "Les fondements de la compétence parentale" if homeweb.language == "fr" else "Foundations of Effective Parenting"
    header = homeweb.header
    header_buttons = header.elements["buttons"]

    # 1: Search and navigate to course
    homeweb.search_and_open_resource(search_term, endpoint=course_endpoint)
    assert homeweb.wait_for_resource_content()
    assert course_endpoint in homeweb.current_url.lower(), \
        f"EXPECTED: '{course_endpoint}' | ACTUAL: {homeweb.current_url}"
    record_output(f"Course loaded | '{search_term}' | {course_endpoint}")

    # 2: Test - Open modal
    homeweb.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"modal\"]")
    assert homeweb.wait_for_modal()

    # 3: Test - Dismiss modal, display course content
    homeweb.click_element(By.CSS_SELECTOR, "[data-bs-dismiss=\"modal\"]")
    assert homeweb.wait_for_course_content()


# BAT-WEB-013 | Homeweb Logout
def test_bat_web_013(homeweb):
    assert homeweb.is_authenticated()
    homeweb.logout()


# BAT-WEB-014 | Homeweb Login - HHI
def test_bat_web_014(homeweb, credentials, env, record_output):
    homeweb.navigate_landing()
    email = credentials["hhi_personal"]["email"]
    password = credentials["hhi_personal"]["password"]

    assert homeweb.is_landing()

    # 1: Test - Sign In - Header
    homeweb.navigate_sign_in()

    # 2: Test - Login - Homeweb - HHI
    quantum = homeweb.quantum
    quantum.login(email, password)
    record_output(f"Login | Email: {email}")
    assert homeweb.wait_for_dashboard(), \
        f"DASHBOARD NOT LOADED: '{homeweb.current_url}'"


# BAT-WEB-015 | SCN - Scenario 1: Resource ONLY [HHI]
def test_bat_web_015(homeweb, record_output):
    assert homeweb.is_authenticated()
    assert homeweb.wait_for_dashboard(), \
        f"DASHBOARD NOT LOADED: '{homeweb.current_url}'"

    # 1: Test - Launch Smart Care Navigation Assessment
    homeweb.navigate_scn_assessment()
    record_output("Smart Care Navigation launched")

    # 2: Test - Complete SCN Assessment - Scenario 1
    homeweb.complete_assessment(logger=record_output)
    assert homeweb.is_assessment_complete()
    homeweb.assert_recommendation_scenario_1()

    homeweb.take_screenshot("scenario1", logger=record_output)

    homeweb.logout()


# BAT-WEB-016 | SCN - Scenario 2: Professional Support & Sentio [DSGDEMO]
def test_bat_web_016(homeweb, quantum, credentials, record_output):

    # 1: Test - Sign In - Header
    assert homeweb.is_landing()
    homeweb.navigate_sign_in()

    # 2: Test - Login - Homeweb - DSGDEMO
    quantum = homeweb.quantum
    email = credentials["dsgdemo_s2"]["email"]
    password = credentials["dsgdemo_s2"]["password"]
    quantum.login(email, password)
    record_output(f"Login | Email: {email}")
    assert homeweb.wait_for_dashboard(), \
        f"DASHBOARD NOT LOADED: '{homeweb.current_url}'"

    # 3: Test - Launch Smart Care Navigation Assessment
    homeweb.navigate_scn_assessment()
    record_output("Smart Care Navigation launched")

    # 4: Test - Complete SCN Assessment - Scenario 2
    homeweb.complete_assessment(logger=record_output)
    assert homeweb.is_assessment_complete()
    homeweb.assert_recommendation_scenario_2()

    homeweb.take_screenshot("scenario2", logger=record_output)


# BAT-WEB-017 | SCN - Scenario 3: Professional Support ONLY [DSGDEMO]
def test_bat_web_017(homeweb, quantum, record_output):
    homeweb.navigate_dashboard()

    # 3: Test - Launch Smart Care Navigation Assessment
    homeweb.navigate_scn_assessment()
    record_output("Smart Care Navigation launched")

    # 4: Test - Complete SCN Assessment - Scenario 3
    flow = [2, 1, 1]
    homeweb.complete_assessment(flow, logger=record_output)
    assert homeweb.is_assessment_complete()
    homeweb.assert_recommendation_scenario_3()

    homeweb.take_screenshot("scenario3", logger=record_output)

    homeweb.logout()


# BAT-WEB-018 | SCN - Scenario 4: Sentio ONLY [DSGDEMO-S3]
def test_bat_web_018(homeweb, quantum, credentials, record_output):
    # 1: Test - Sign In - Header
    assert homeweb.is_landing()
    homeweb.navigate_sign_in()

    # 2: Test - Login - Homeweb - DSGDEMO
    quantum = homeweb.quantum
    email = credentials["dsgdemo_s3"]["email"]
    password = credentials["dsgdemo_s3"]["password"]
    quantum.login(email, password)
    record_output(f"Login | Email: {email}")
    assert homeweb.wait_for_dashboard(), \
        f"DASHBOARD NOT LOADED: '{homeweb.current_url}'"

    # 3: Test - Launch Smart Care Navigation Assessment
    homeweb.navigate_scn_assessment()
    record_output("Smart Care Navigation launched")

    # 4: Test - Complete SCN Assessment - Scenario 4
    homeweb.complete_assessment(logger=record_output)
    assert homeweb.is_assessment_complete()
    homeweb.assert_recommendation_scenario_4()

    homeweb.take_screenshot("scenario4", logger=record_output)


# BAT-WEB-019 | SCN - Scenario 5: Legal Flow [DSGDEMO]
def test_bat_web_019(homeweb, quantum, record_output):
    homeweb.navigate_dashboard()

    # 3: Test - Launch Smart Care Navigation Assessment
    homeweb.navigate_scn_assessment()
    record_output("Smart Care Navigation launched")

    # 4: Test - Complete SCN Assessment - Scenario 5
    flow = [3, 4]
    homeweb.complete_assessment(flow, logger=record_output)
    assert homeweb.is_assessment_complete()
    homeweb.assert_recommendation_scenario_5()

    homeweb.take_screenshot("scenario5", logger=record_output)

    # homeweb.logout()


# BAT-WEB-020 | SCN - Scenario 6: Financial Flow [DSGDEMO]
def test_bat_web_020(homeweb, quantum, record_output):
    homeweb.navigate_dashboard()

    # 3: Test - Launch Smart Care Navigation Assessment
    homeweb.navigate_scn_assessment()
    record_output("Smart Care Navigation launched")

    # 4: Test - Complete SCN Assessment - Scenario 6
    flow = [4, 3]
    homeweb.complete_assessment(flow, logger=record_output)
    assert homeweb.is_assessment_complete()
    homeweb.assert_recommendation_scenario_6()

    homeweb.take_screenshot("scenario6", logger=record_output)

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
#     homeweb.assert_recommendation_scenario_2()
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

# Copyright © 2026 - Homewood Health Inc.

################# BUILD ACCEPTANCE ################
##################### HOMEWEB #####################
################# NEW PORTAL - BETA ###############
from datetime import datetime

import pytest
from selenium.webdriver.common.by import By


## CORE MODULES
# TODO | Registration
# [DONE] Standard | DSGDEMO
# TODO | MFA - Canada Post Corporation
# TODO | Custom - LSO, Alumni, Equitable
# TODO | Eligibility List - Canada Post Corporation
# TODO | Additional Fields - Alumni, Equitable, etc.
# TODO | Registration/Invitation Code - Dependents invite?? PAC?

# TODO - Login
# [DONE] - DSGDEMO
# [DONE] - HHI

# TODO-P1 | Dashboard - S1
# TODO-P1 | Onboarding [WIP]

# TODO-P1 | Dashboard - S2

# TODO-P1 Dashboard - S3

# TODO-P2 Discover - Mental Health
# TODO-P2 Discover - Wellness
# TODO-P2 Discover - Work-Life

# TODO-P2 Journey - Plans
# TODO-P2 Journey - Sessions
# TODO-P2 Journey - Appointments

# [DONE] Smart Care Navigation
# [DONE] - Scenario 1: Resource ONLY
# [DONE] - Scenario 2: Professional Support & Sentio
# [DONE] - Scenario 3: Professional Support ONLY
# [DONE] - Scenario 4: Sentio ONLY
# [DONE] - Scenario 5: Legal Flow
# [DONE] - Scenario 6: Financial Flow

# TODO-P1 Booking [NEXT]
# TODO-P1 Profile [NEXT]

# [DONE] Library
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
    if input("Include new registration in this run? (y/n): ").strip().lower() != "y":
        pytest.skip("Registration skipped by user")

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
    # 1: Test - Sign In - Button
    homeweb.navigate_landing()
    buttons = homeweb.public["elements"]["buttons"]
    quantum = homeweb.quantum
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


# BAT-WEB-021 | Navigate to Messages
def test_bat_web_021(homeweb):
    homeweb.is_authenticated()

    # 1: Test - Navigate to Messages
    homeweb.navigate_messages()

    homeweb.logout()


# BAT-WEB-022 | Embedded - Mobile Resources
def test_bat_web_022(homeweb):
    lang_prefix = f"/{homeweb.language}" if homeweb.language == "fr" else ""
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

# # TODO: BAT-WEB-xxx | HHI Cancel Active Services [hhi-employee@demo.com]
# # [SKIP - Andrew request]
# def test_bat_web_xxx(homeweb, quantum, credentials, env):
#     pytest.skip("Skipping Cancel Active Services -> Andrew request")
#
#
# # TODO: BAT-WEB-xxx | Live Chat
# # [SKIP - MANUAL]
# def test_bat_web_xxx(homeweb, quantum, credentials, env):
#     pytest.skip("Skipping Live Chat -> MANUAL TEST")
#
#
# # TODO: BAT-WEB-xxx | Create Pathfinder Booking
# # [SKIP - WIP]
# def test_bat_web_xxx(homeweb, credentials, env):
#     pytest.skip("Skipping Create Booking -> WIP")
#
#
# # TODO: BAT-WEB-xxx | Complete Pathfinder Booking
# # [SKIP - WIP]
# def test_bat_web_xxx(homeweb, credentials):
#     pytest.skip("Skipping Complete Booking -> WIP")
#

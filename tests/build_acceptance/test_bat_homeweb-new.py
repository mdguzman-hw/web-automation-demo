# Copyright © 2026 - Homewood Health Inc.

################# BUILD ACCEPTANCE ################
##################### HOMEWEB #####################
################# NEW PORTAL - BETA ###############
from datetime import datetime

import pytest
from selenium.webdriver.common.by import By


### CORE MODULES ###
## HOLD | Registration
# DONE] Standard | DSGDEMO
# HOLD | MFA - Canada Post Corporation
# HOLD | Custom - LSO, Alumni, Equitable
# HOLD | Eligibility List - Canada Post Corporation
# HOLD | Additional Fields - Alumni, Equitable, etc.
# HOLD | Registration/Invitation Code - Dependents invite?? PAC?

## DONE | Login
# DONE | DSGDEMO
# DONE | HHI

## HOLD | Dashboard - S1

## HOLD | Dashboard - S2

## HOLD | Dashboard - S3

# TODO-P2 Discover - Mental Health
# TODO-P2 Discover - Wellness
# TODO-P2 Discover - Work-Life

# DONE | Journey - Plans
# DONE | Journey - Sessions
# TODO-P3 Journey - Appointments

# DONE | Smart Care Navigation
# DONE | Scenario 1: Resource ONLY
# DONE | Scenario 2: Professional Support & Sentio
# DONE | Scenario 3: Professional Support ONLY
# DONE | Scenario 4: Sentio ONLY
# DONE | Scenario 5: Legal Flow
# DONE | Scenario 6: Financial Flow

# DONE | Booking

# TODO-P1 Profile

# DONE | Library
# DONE | Resource Library
# DONE | Primary Category
# DONE | Subcategory

# DONE | Messages


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


# BAT-WEB-004 | Homeweb Login - FTT
def test_bat_web_004(homeweb, latest_registered_account, record_output):
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


# BAT-WEB-005 | Complete Onboarding - FTT
def test_bat_web_005(homeweb, record_output, registered_this_run):
    if not registered_this_run:
        pytest.skip("Skipping — no account registered this run (test_bat_web_003 did not execute)")
    assert homeweb.is_authenticated()
    homeweb.complete_onboarding(logger=record_output)
    assert homeweb.wait_for_dashboard()


# BAT-WEB-006 | Create and Complete Booking - FTT
def test_bat_web_006(homeweb, latest_registered_account, record_output, update_account_dashboard):
    assert homeweb.is_authenticated()

    # 1: Test - Validate S2 Dashboard State
    homeweb.navigate_dashboard()
    dashboard_state = homeweb.get_dashboard_state()
    assert dashboard_state == "S2", \
        f"EXPECTED: Dashboard S2 | ACTUAL: {dashboard_state} (onboarding may not be complete)"

    # 2: Test - Launch Smart Care Navigation Assessment
    homeweb.navigate_scn_assessment()
    record_output("Smart Care Navigation launched")

    # 3: Test - Complete SCN Assessment - Scenario 2
    homeweb.complete_assessment(logger=record_output)
    assert homeweb.is_assessment_complete()
    homeweb.assert_recommendation_scenario_2()

    # 4: Test - Create Booking
    homeweb.get_started()
    assert homeweb.wait_for_book_for()
    homeweb.complete_book_for(0)
    assert homeweb.wait_for_booking_create()
    email = latest_registered_account["Email"]
    homeweb.complete_booking_contact_form(
        email=email,
        phone="1234567890",
        address_type="Work",  # Home, Work, Other
        street_address="1234567 Homewood Ave",
        postal_code="T2X 6V7",
        message_permission="1",
    )
    assert homeweb.wait_for_provider_matching()
    homeweb.select_first_available_provider()
    assert homeweb.wait_for_booking_details()
    homeweb.select_booking_options()
    assert homeweb.wait_for_booking_confirm()
    homeweb.confirm_booking()

    homeweb.navigate_dashboard()
    dashboard_state = homeweb.get_dashboard_state()
    assert dashboard_state == "S3", \
        f"EXPECTED: Dashboard S3 | ACTUAL: {dashboard_state} (no appointments)"
    update_account_dashboard("S3")


# BAT-WEB-007 | Homeweb Resource
def test_bat_web_007(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = homeweb.base_url + "/" + homeweb.language + "/user/articles/56252b81e40e6f50062aa714"
    homeweb.driver.get(resource_target)
    assert homeweb.wait_for_resource_content(), \
        f"RESOURCE NOT LOADED"


# BAT-WEB-008 | Resource Library
def test_bat_web_008(homeweb, record_output):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to Resources
    homeweb.navigate_library()
    assert homeweb.wait_for_resources()

    # 2: Test - Primary categories are visible
    categories = homeweb.get_resource_categories()
    assert len(categories) > 0
    category_names = [c.text.strip() for c in categories]
    record_output(f"Resource categories ({len(category_names)}): {', '.join(category_names)}")


# BAT-WEB-009 | Primary Category
def test_bat_web_009(homeweb, record_output):
    assert homeweb.wait_for_resources()

    # 1: Test - Click first primary category
    categories = homeweb.get_resource_categories()
    first_category = categories[0]
    category_name = first_category.text.strip()
    record_output(f"Category: {category_name}")
    first_category.click()

    # 2: Test - Category page loaded
    assert homeweb.wait_for_resources()


# BAT-WEB-010 | Subcategory
def test_bat_web_010(homeweb, record_output):
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


# BAT-WEB-011 | Search
def test_bat_web_011(homeweb):
    assert homeweb.wait_for_resources()

    # 1: Test - Perform search
    homeweb.search_resources("mental health")
    assert homeweb.wait_for_search_results()


# BAT-WEB-012 | Kickouts
def test_bat_web_012(homeweb, env, record_output):
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


# BAT-WEB-013 | Sentio Kickout
def test_bat_web_013(homeweb, env, record_output):
    if env == "staging":
        pytest.skip("Skipping Sentio kickout — not applicable for staging")
    sentio_endpoint = "/resources/62c5a1e929ed9c1608d0434b"
    search_term = "Sentio par Homewood Santé" if homeweb.language == "fr" else "Sentio by Homewood Health"

    assert homeweb.wait_for_resources()

    # 1: Test - Search and navigate to Sentio resource
    homeweb.search_and_open_resource(search_term)
    assert homeweb.wait_for_resource_content(), f"RESOURCE NOT LOADED: '{search_term}'"
    assert sentio_endpoint in homeweb.current_url.lower(), \
        f"EXPECTED: '{sentio_endpoint}' | ACTUAL: {homeweb.current_url}"
    record_output(f"Sentio resource loaded | {sentio_endpoint}")

    # 2: Test - Sentio transfer kickout
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    homeweb.handle_transfer_consent()
    assert homeweb.wait_for_sentio_transfer(), "SENTIO TRANSFER FAILED"
    record_output("Sentio kickout confirmed")
    homeweb.go_back()


# BAT-WEB-014 | Course Consent
def test_bat_web_014(homeweb, record_output):
    homeweb.navigate_library()
    assert homeweb.wait_for_resources()
    course_endpoint = "/resources/564a36083392100756dd3e32"
    search_term = "Les fondements de la compétence parentale" if homeweb.language == "fr" else "Foundations of Effective Parenting"

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


# BAT-WEB-015 | Homeweb Logout
def test_bat_web_015(homeweb):
    assert homeweb.is_authenticated()
    homeweb.logout()


# BAT-WEB-016 | Homeweb Login - HHI
def test_bat_web_016(homeweb, credentials, record_output):
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


# BAT-WEB-017 | SCN - Scenario 1: Resource ONLY [HHI]
def test_bat_web_017(homeweb, record_output):
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


# BAT-WEB-018 | SCN - Scenario 2: Professional Support & Sentio [DSGDEMO]
def test_bat_web_018(homeweb, credentials, record_output):
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


# BAT-WEB-019 | SCN - Scenario 3: Professional Support ONLY [DSGDEMO]
def test_bat_web_019(homeweb, record_output):
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


# BAT-WEB-020 | SCN - Scenario 4: Sentio ONLY [DSGDEMO-S3]
def test_bat_web_020(homeweb, credentials, record_output):
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


# BAT-WEB-021 | SCN - Scenario 5: Legal Flow [DSGDEMO]
def test_bat_web_021(homeweb, record_output):
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


# BAT-WEB-022 | SCN - Scenario 6: Financial Flow [DSGDEMO]
def test_bat_web_022(homeweb, record_output):
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


# # BAT-WEB-023 | End Service [DSGDEMO-S3]
# def test_bat_web_023(homeweb, credentials, record_output, update_account_dashboard):
#     # 1: Test - Sign In - Header
#     homeweb.navigate_landing()
#     homeweb.navigate_sign_in()
#
#     # 2: Test - Login - Homeweb - DSGDEMO
#     quantum = homeweb.quantum
#     email = credentials["mdg_test"]["email"]
#     password = credentials["mdg_test"]["password"]
#     quantum.login(email, password)
#     record_output(f"Login | Email: {email}")
#     assert homeweb.wait_for_dashboard(), \
#         f"DASHBOARD NOT LOADED: '{homeweb.current_url}'"
#     homeweb.navigate_dashboard()
#
#     # 1: Assert S3 dashboard (active session required)
#     dashboard_state = homeweb.get_dashboard_state()
#     assert dashboard_state == "S3", \
#         f"EXPECTED: Dashboard S3 | ACTUAL: {dashboard_state} (no active session to end)"
#
#     # 2: Quick Access — scroll to Sessions
#     homeweb.navigate_sessions()
#
#     # 3: Assert at least one active scheduled session
#     homeweb.assert_active_session()
#
#     # 4: Click View Details -> /homeweb/appointment
#     homeweb.click_view_details()
#     assert homeweb.wait_for_appointment_page()
#     record_output(f"Appointment page: {homeweb.current_url}")
#
#     # 5: Click 'end services' link in Modify section -> /homeweb/services/end
#     homeweb.click_end_services_link()
#
#     # 6: Confirmation page — click Yes
#     assert homeweb.wait_for_end_service_confirmation()
#     homeweb.confirm_end_service()
#
#     # 7: Survey — select random reason (auto-navigates to dashboard)
#     homeweb.complete_end_service_survey()
#
#     # 8: Assert S2 — service still active, no sessions
#     assert homeweb.wait_for_dashboard()
#     dashboard_state = homeweb.get_dashboard_state()
#     assert dashboard_state == "S2", \
#         f"EXPECTED: Dashboard S2 after ending service | ACTUAL: {dashboard_state}"
#     record_output(f"Dashboard state after end service: {dashboard_state}")
#
#     # 9: Navigate to Journey via header
#     homeweb.navigate_journey()
#     assert homeweb.wait_for_journey()
#
#     # 10: Filter by Open plans
#     homeweb.filter_journey_plans("CASE_OPEN")
#
#     # 11: Assert no open plans — confirms service/plan is now closed
#     assert homeweb.assert_no_plans_match_filter()
#     record_output("Journey: No open plans confirmed — service ended successfully")
#
#     # 12: Re-book — SCN Scenario 2 -> Professional Support & Sentio
#     homeweb.navigate_dashboard()
#     homeweb.navigate_scn_assessment()
#     record_output("Smart Care Navigation launched")
#     homeweb.complete_assessment(logger=record_output)
#     assert homeweb.is_assessment_complete()
#     homeweb.assert_recommendation_scenario_2()
#     homeweb.take_screenshot("023_scenario2", logger=record_output)
#
#     # 13: Create Booking
#     homeweb.get_started()
#     assert homeweb.wait_for_book_for()
#     homeweb.complete_book_for(0)
#     assert homeweb.wait_for_booking_create()
#     email = credentials["dsgdemo_s3"]["email"]
#     homeweb.complete_booking_contact_form(
#         email=email,
#         phone="1234567890",
#         address_type="Work",
#         street_address="1234567 Homewood Ave",
#         postal_code="T2X 6V7",
#         message_permission="1",
#         province="Ontario",
#         city="Guelph",
#     )
#     assert homeweb.wait_for_provider_matching()
#     homeweb.select_first_available_provider()
#     assert homeweb.wait_for_booking_details()
#     homeweb.select_booking_options()
#     assert homeweb.wait_for_booking_confirm()
#     homeweb.confirm_booking()
#
#     # 14: Assert S3 restored
#     homeweb.navigate_dashboard()
#     dashboard_state = homeweb.get_dashboard_state()
#     assert dashboard_state == "S3", \
#         f"EXPECTED: Dashboard S3 after re-booking | ACTUAL: {dashboard_state}"
#     update_account_dashboard("S3")
#     record_output(f"Re-booking complete — Dashboard: {dashboard_state}")


# # BAT-WEB-024 | Cancel Appointment [DSGDEMO-S3]
# def test_bat_web_024(homeweb, credentials, record_output, update_account_dashboard):
#     homeweb.navigate_dashboard()
#
#     # 1: Assert S3 — note Appointment ID
#     dashboard_state = homeweb.get_dashboard_state()
#     assert dashboard_state == "S3", \
#         f"EXPECTED: Dashboard S3 | ACTUAL: {dashboard_state} (no active session to cancel)"
#     appointment_id = homeweb.get_active_appointment_id()
#     record_output(f"Active Appointment ID: {appointment_id}")
#
#     # 2: Journey → Plans → filter Open → note Plan ID
#     homeweb.navigate_journey()
#     assert homeweb.wait_for_journey()
#     homeweb.filter_journey_plans("CASE_OPEN")
#     plan_id = homeweb.get_open_plan_id()
#     record_output(f"Open Plan ID: {plan_id}")
#
#     # 3: Journey → Sessions tab → filter Scheduled
#     homeweb.navigate_journey_sessions()
#     homeweb.filter_journey_sessions("SCHEDULED")
#
#     # 4: Click View Details on matching appointment
#     homeweb.click_session_view_details(appointment_id)
#     assert homeweb.wait_for_appointment_page()
#
#     # 5: Click Cancel → "Are you sure?" section appears
#     homeweb.click_cancel_appointment_btn()
#
#     # 6: Click "Yes, Cancel Appointment" → /homeweb/booking/cancel
#     homeweb.click_yes_cancel_appointment()
#
#     # 7: Confirm cancellation → navigates to dashboard
#     homeweb.confirm_cancel_appointment()
#
#     # 8: Assert S2 — service still active, appointment cancelled
#     assert homeweb.wait_for_dashboard()
#     dashboard_state = homeweb.get_dashboard_state()
#     assert dashboard_state == "S2", \
#         f"EXPECTED: Dashboard S2 after cancel | ACTUAL: {dashboard_state}"
#     record_output(f"Dashboard after cancel: {dashboard_state}")
#
#     # 9: Journey → Plans → filter Open → confirm Plan ID still exists (service not ended)
#     homeweb.navigate_journey()
#     assert homeweb.wait_for_journey()
#     homeweb.filter_journey_plans("CASE_OPEN")
#     assert homeweb.assert_plan_id_exists(plan_id)
#     record_output(f"Plan ID {plan_id} confirmed — service still active after appointment cancel")
#
#     # 10: Re-book — Get Started from open plan card (no SCN assessment)
#     homeweb.get_started_from_journey()
#     assert homeweb.wait_for_provider_matching()
#     homeweb.select_first_available_provider()
#     assert homeweb.wait_for_booking_details()
#     homeweb.select_booking_options()
#     assert homeweb.wait_for_booking_confirm()
#     homeweb.confirm_booking()
#
#     # 11: Assert S3 restored
#     homeweb.navigate_dashboard()
#     dashboard_state = homeweb.get_dashboard_state()
#     assert dashboard_state == "S3", \
#         f"EXPECTED: Dashboard S3 after re-booking | ACTUAL: {dashboard_state}"
#     update_account_dashboard("S3")
#     record_output(f"Re-booking complete — Dashboard: {dashboard_state}")

# # BAT-WEB-025 | Update Profile [DSGDEMO-S3]
# def test_bat_web_025(homeweb, record_output):
#     pytest.skip("WIP->Update Profile")
#
#
# # BAT-WEB-026 | Discover [DSGDEMO-S3]
# def test_bat_web_026(homeweb, record_output):
#     pytest.skip("WIP->Discover")
#
#
# # BAT-WEB-027 | Journey [DSGDEMO-S3]
# def test_bat_web_027(homeweb, record_output):
#     pytest.skip("WIP->Journey")
#
#
# BAT-WEB-026 | Navigate to Messages
def test_bat_web_028(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to Messages
    homeweb.navigate_messages()

    homeweb.logout()

# BAT-WEB-027 | Embedded - Mobile Resources
def test_bat_web_029(homeweb):
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

# TODO: BAT-WEB-xxx | Live Chat [SKIP - MANUAL]
# def test_bat_web_xxx_livechat():
#     pytest.skip("Skipping Live Chat -> MANUAL")

# TODO: BAT-WEB-xxx | HHI Cancel Active Services [hhi-employee@demo.com]
# ONLY FOR PROD - No need to implement now, only testing BETA
# [SKIP - Andrew request]
# def test_bat_web_xxx_hhi_cancel_service(homeweb, credentials, env):
#     pytest.skip("Skipping Cancel Active Services -> Andrew request")
#
#

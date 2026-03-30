# Copyright © 2026 - Homewood Health Inc.
################# SMOKE ################
################ HOMEWEB ###############
import pytest
from selenium.webdriver.common.by import By


# REGISTRATION
# TODO: SMOKE-001 | Homewood Registration - Initial State
# TODO: SMOKE-002	| Create an account

# LANDING PAGE - Homeweb Anonymouse
# TEST: Homeweb Landing - Initial State
def test_smoke_homeweb_003(homeweb):
    # 1: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()
    assert homeweb.is_landing()
    assert homeweb.wait_for_landing()


# DASHBOARD
# TEST: Dashboard - Initial State
def test_smoke_homeweb_004(homeweb, credentials):
    assert homeweb.is_landing()
    assert homeweb.wait_for_landing()
    buttons = homeweb.public["elements"]["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Button
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in homeweb.current_url.lower()

    # 2: Test - Login - Homeweb - Personal
    # quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert homeweb.wait_for_dashboard()

    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    # TODO: Should the test assertion validate all UI elements listed in spreadsheet?


# PULSECHECK
# TEST: Pulsecheck - Initial State
def test_smoke_homeweb_005(homeweb, credentials):
    assert homeweb.is_authenticated()
    assert homeweb.wait_for_dashboard()

    # 1: Test - Retrieve Dashboard Tiles
    # TODO: Investigate if this is expected
    expected = 6 if homeweb.language == "fr" else 8
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

    # 2: Test - Navigate Wellness
    wellness_tile = dashboard_tiles[3]
    wellness_tile.navigate()
    assert homeweb.wait_for_pulsecheck()
    # TODO: Should the test assertion validate all UI elements listed in spreadsheet?


# TEST: Pulsecheck Recommendation - Check In
def test_smoke_homeweb_006(homeweb):
    pytest.skip("Skipping for now")
    assert homeweb.is_authenticated()
    assert homeweb.wait_for_pulsecheck()

    # TODO: Navigate through header

    # TODO: Click Check-In

    # TODO Test - Pulse Check
    homeweb.complete_pulsecheck()

    # TODO Test - Mood Check
    homeweb.complete_moodcheck()


# PATHFINDER
# TEST: Pathfinder - Initial State
def test_smoke_homeweb_007(homeweb):
    assert homeweb.is_authenticated()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    expected = 6 if homeweb.language == "fr" else 8
    assert len(homeweb.get_dashboard_tiles()) == expected

    # 1: Test - Check and cancel active services
    appointments = homeweb.get_active_services()
    topics = [a.topic for a in appointments]

    for topic in topics:
        homeweb.end_services(topic)
        assert homeweb.wait_for_dashboard()
        remaining = homeweb.get_active_services()
        assert not any(a.topic == topic for a in remaining)

    # 2: Test - Navigate Wellness
    assert homeweb.wait_for_dashboard()
    dashboard_tiles = homeweb.get_dashboard_tiles()
    pathfinder_tile = dashboard_tiles[0]
    pathfinder_tile.navigate()
    assert homeweb.wait_for_assessment()


# TEST: Launch Pathfinder - Same as 007 ???
def test_smoke_homeweb_008(homeweb):
    pytest.skip("Skipping for now")
    assert homeweb.is_authenticated()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    expected = 6 if homeweb.language == "fr" else 8
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

    # 2: Test - Navigate Wellness
    pathfinder_tile = dashboard_tiles[0]
    pathfinder_tile.navigate()
    assert homeweb.wait_for_assessment()


# TEST: Assessment Start
def test_smoke_homeweb_009(homeweb):
    assert homeweb.is_authenticated()
    assert homeweb.wait_for_assessment()

    homeweb.complete_assessment()
    assert homeweb.is_assessment_complete()


# TEST: 5 star rating pages
def test_smoke_homeweb_010(homeweb):
    assert homeweb.is_authenticated()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    homeweb.navigate_recommendations()
    assert homeweb.wait_for_recommendation()

    homeweb.navigate_rating()
    assert homeweb.wait_for_rating()

    homeweb.complete_rating("5")
    assert homeweb.wait_for_booking_create()


# TEST: Intake questions
def test_smoke_homeweb_011(homeweb, credentials):
    assert homeweb.is_authenticated()
    assert homeweb.wait_for_booking_create()
    email = credentials["sentio"]["email"]

    homeweb.complete_booking_create_form()
    assert homeweb.wait_for_service_confirm()

    homeweb.complete_service_confirm_form(email)
    assert homeweb.wait_for_booking_digest()


# TEST: Booking calendar
def test_smoke_homeweb_012(homeweb):
    assert homeweb.is_authenticated()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    # 1: Test - Check Active Services
    appointments = homeweb.get_active_services()
    topics = [a.topic for a in appointments]
    print(topics)

    # 2: Test - Continue booking for first appointment available
    homeweb.continue_booking(topics[0])
    assert homeweb.wait_for_booking_digest()

    # 3: Test - Select
    homeweb.select_provider()
    assert homeweb.wait_for_booking_details()

    homeweb.select_booking_options()
    assert homeweb.wait_for_booking_confirm()

    homeweb.confirm_booking()


# TODO: SMOKE-013	| Cancel
# TODO: SMOKE-014	| More options
# TODO: SMOKE-015	| Reschedule

# TEST: End Services
def test_smoke_homeweb_016(homeweb):
    assert homeweb.is_authenticated()
    homeweb.navigate_dashboard()
    assert homeweb.wait_for_dashboard()

    # 1: Test - Check and cancel active services
    appointments = homeweb.get_active_services()
    topics = [a.topic for a in appointments]

    for topic in topics:
        homeweb.end_services(topic)
        assert homeweb.wait_for_dashboard()
        remaining = homeweb.get_active_services()
        assert not any(a.topic == topic for a in remaining)

    assert homeweb.is_authenticated()
    header = homeweb.header
    header_buttons = header.elements["buttons"]

    # 2: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 3: Test - Logout
    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb.wait_for_logout()
    homeweb.navigate_landing()


# LANDING PAGE - CUSTOM
# TEST: Enbridge Landing - Initial State
def test_smoke_homeweb_017(homeweb, credentials, env):

    assert not homeweb.is_authenticated()
    homeweb.navigate_landing("enbridge")
    assert homeweb.wait_for_landing()

    # header = homeweb.header
    # header_buttons = header.elements["buttons"]
    # paths = header.paths["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Header
    homeweb.click_element(By.CSS_SELECTOR, "[aria-label=\"Sign In\"]")
    homeweb.complete_enbridge_login_modal()
    assert quantum.domain in homeweb.current_url.lower()

    # NO BETA ACCESS
    if env == "beta":
        pytest.skip(f"Skipping LSO Login - No {env} access")

    # 2: Test - Login - Homeweb - LSO Test
    email = credentials["lso_test"]["email"]
    password = credentials["lso_test"]["password"]
    quantum.login(email, password)
    assert homeweb.wait_for_dashboard()

    # 3: Test - Retrieve Dashboard Tiles
    # TODO: Investigate if this is expected
    # expected = 6 if homeweb.language == "fr" else 8
    # dashboard_tiles = homeweb.get_dashboard_tiles()
    # actual = len(dashboard_tiles)
    # assert actual == expected
    # for tile in dashboard_tiles:
    #     tile.navigate()
    #     assert tile.href in homeweb.current_url.lower()

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


# TEST: Suncor Landing - Initial State
def test_smoke_homeweb_018(homeweb):
    assert not homeweb.is_authenticated()
    homeweb.navigate_landing("suncor")
    assert homeweb.wait_for_landing()


# TEST: LSO Landing- Initial State
def test_smoke_homeweb_019(homeweb):
    assert not homeweb.is_authenticated()
    homeweb.navigate_landing("map")
    assert homeweb.wait_for_landing()


# TEST: EQ Landing- Initial State
def test_smoke_homeweb_020(homeweb):
    assert not homeweb.is_authenticated()
    homeweb.navigate_landing("equitable")
    assert homeweb.wait_for_landing()


# TEST: ALUMNI Landing- Initial State
def test_smoke_homeweb_021(homeweb):
    assert not homeweb.is_authenticated()
    homeweb.navigate_landing("alumni")
    assert homeweb.wait_for_landing()


# TEST: Pacific Blue Cross Landing- Initial State
def test_smoke_homeweb_022(homeweb):
    assert not homeweb.is_authenticated()
    homeweb.navigate_landing("pbc")
    assert homeweb.wait_for_landing()


# RESOURCES
# TEST: External redirects for homeweb
def test_smoke_homeweb_023(homeweb, quantum, env, credentials):
    assert not homeweb.is_authenticated()
    homeweb.navigate_landing()
    assert homeweb.wait_for_landing()

    header = homeweb.header
    header_buttons = header.elements["buttons"]
    paths = header.paths["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Header
    header.click_element(By.CLASS_NAME, header_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - DSG Demo
    email = credentials["sentio"]["email"]
    password = credentials["sentio"]["password"]
    quantum.login(email, password)
    assert homeweb.wait_for_dashboard()

    # 1: Test - Retrieve Dashboard Tiles
    # TODO: Investigate if this is expected
    # expected = 6 if homeweb.language == "fr" else 8
    # dashboard_tiles = homeweb.get_dashboard_tiles()
    # actual = len(dashboard_tiles)
    # assert actual == expected
    # for tile in dashboard_tiles:
    #     tile.navigate()
    #     assert tile.href in homeweb.current_url.lower()


# TODO: SMOKE-024	| External redirects for homeweb LSO
# TODO: SMOKE-025	| External redirects for homeweb Enbridge
# TODO: SMOKE-026	| External redirects for homeweb EQ
# TODO: SMOKE-027	| External redirects for homeweb Suncor
# TODO: SMOKE-028	| External redirects for homeweb PBC

# MESSAGES
# TODO: SMOKE-029	| Initial page state
# TODO: SMOKE-030	| Message Received
# TODO: SMOKE-031	| Message Received
# TODO: SMOKE-032	| Message Received
# TODO: SMOKE-033	| Send Message
# TODO: SMOKE-034	| Sync
# TODO: SMOKE-035	| Change language

# IDENTITY
# TODO: SMOKE-036	| Login in test
# TODO: SMOKE-037	| Forgot password
# TODO: SMOKE-038	| Footer tests
# TEST:Logout
def test_smoke_homeweb_039(homeweb):
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

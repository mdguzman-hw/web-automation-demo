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
    dashboard_tiles = homeweb.get_dashboard_tiles()
    assert len(dashboard_tiles) == expected

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
# TODO: SMOKE-039	| Logout

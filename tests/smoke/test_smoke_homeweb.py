# Copyright © 2026 - Homewood Health Inc.
################# SMOKE ################
################ HOMEWEB ###############
from selenium.webdriver.common.by import By


# REGISTRATION
# TODO: SMOKE-001 | Homewood Registration - Initial State
# TODO: SMOKE-002	| Create an account

# LANDING PAGE - Homeweb Anonymouse
# TODO: SMOKE-003	| Homeweb Landing - Initial State
def test_smoke_homeweb_003(homeweb):
    # 1: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()
    assert homeweb.is_landing()

# DASHBOARD
# TODO: SMOKE-004	| Dashboard - Initial State
def test_smoke_homeweb_004(homeweb, credentials):
    assert homeweb.is_landing()
    buttons = homeweb.public["elements"]["buttons"]
    quantum = homeweb.quantum

    # 1: Test - Sign In - Button
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in homeweb.current_url.lower()

    # 2: Test - Login - Homeweb - Personal
    # quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert homeweb.wait_for_dashboard()

    # TODO: Should the test assertion validate all UI elements listed in spreadsheet?

# PULSECHECK
# TODO: SMOKE-005	| Initial State
# TODO: SMOKE-006	| PulseCheck Reccommendation - Check In

# PATHFINDER
# TODO: SMOKE-007	| Initial State
# TODO: SMOKE-008	| Launch Pathfinder
# TODO: SMOKE-009	| Assessment Start
# TODO: SMOKE-010	| 5 star rating pages
# TODO: SMOKE-011	| Intake questions
# TODO: SMOKE-012	| Booking calendar
# TODO: SMOKE-013	| Booking calendar
# TODO: SMOKE-014	| More options
# TODO: SMOKE-015	| Booking calendar
# TODO: SMOKE-016	| Booking calendar

# LANDING PAGE - Other
# TODO: SMOKE-017	| Enbridge Landing - Initial State
# TODO: SMOKE-018	| Suncor Landing - Initial State
# TODO: SMOKE-019	| LSO Landing- Initial State
# TODO: SMOKE-020	| EQ Landing- Initial State
# TODO: SMOKE-021	| ALUMNI Landing- Initial State
# TODO: SMOKE-022	| Pacific Blue Cross Landing- Initial State

# RESOURCES
# TODO: SMOKE-023	| External redirects for homeweb
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

################# BUILD ACCEPTANCE ################
############## SENTIO BETA - CLIENT ###############
from selenium.webdriver.common.by import By


def test_bat_web_012(sentio_beta_client):
    sentio_beta_client.navigate_landing()
    assert sentio_beta_client.landing_url in sentio_beta_client.current_url.lower()


def test_bat_web_013(sentio_beta_client, quantum, credentials):
    assert sentio_beta_client._is_landing
    elements = sentio_beta_client.landing_elements

    sentio_beta_client.click_element(By.LINK_TEXT, elements["get_started"])
    assert quantum.base_url + "/" + sentio_beta_client.language + "/login" in sentio_beta_client.current_url.lower()

    sentio_beta_client.go_back()
    sentio_beta_client.click_element(By.LINK_TEXT, elements["login"])
    assert quantum.base_url + "/" + sentio_beta_client.language + "/login" in sentio_beta_client.current_url.lower()

    quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert sentio_beta_client.wait_for_dashboard()

    in_progress_programs = sentio_beta_client.in_progress_programs()

    for program in in_progress_programs:
        sentio_beta_client.withdraw_program(program)
        assert sentio_beta_client.wait_for_dashboard()


def test_bat_web_014(sentio_beta_client):
    assert sentio_beta_client._is_authenticated

    programs = sentio_beta_client.available_programs()
    assert programs

    completed_status = {
        "en": "Completed",
        "fr": "Exercice terminé"
    }
    # Filter programs that are Completed or None
    valid_programs = [
        p for p in programs
        if p.status is None or p.status == completed_status[sentio_beta_client.language].upper()
    ]
    assert valid_programs, "No completed or unstarted programs available"

    # Can modify this to be a specific program, if required
    # Pick random program to test
    # test_program = random.choice(valid_programs)

    # Specify program to test
    test_program = next(
        p for p in valid_programs
        if p.title == sentio_beta_client.programs["mental_health"]
    )

    sentio_beta_client.navigate_overview(test_program.title)
    assert test_program.href in sentio_beta_client.current_url.lower()

    sentio_beta_client.navigate_assessment()
    assert "/assessments" and "take" in sentio_beta_client.current_url.lower()

    sentio_beta_client.complete_assessment()
    assert "/assessments" and "results" in sentio_beta_client.current_url.lower()

    tiers = sentio_beta_client.available_tiers()
    provinces = sentio_beta_client.available_provinces()
    assert tiers
    assert provinces

    # Can modify to be a specific tier and province, if required
    # Pick random program to test
    # test_tier = random.choice(tiers)
    # test_province = random.choice(provinces)

    # Specify program tier and province
    test_tier = tiers["TIER_2"]
    test_province = provinces["Prince Edward Island"]
    sentio_beta_client.start_program(test_tier, test_province)
    sentio_beta_client.wait_for_activity_content()

    sentio_beta_client.navigate_dashboard()
    in_progress_programs = sentio_beta_client.in_progress_programs()
    assert any(
        p.title == test_program.title
        for p in in_progress_programs
    )


def test_bat_web_015(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    in_progress_programs = sentio_beta_client.in_progress_programs()
    assert in_progress_programs, "No in_progress programs available"

    # Can modify to be a specific program, if required
    # test_program = random.choice(in_progress_programs)

    # Specify program to test
    test_program = next(
        p for p in in_progress_programs
        if p.title == sentio_beta_client.programs["mental_health"]
    )

    sentio_beta_client.continue_program(test_program.title)
    assert test_program.href_toc in sentio_beta_client.current_url.lower()


def test_bat_web_016(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    sentio_beta_client.navigate_dashboard()
    assert sentio_beta_client.dashboard_endpoint in sentio_beta_client.current_url.lower()

    sentio_beta_client.continue_program(sentio_beta_client.programs["mental_health"])
    assert sentio_beta_client.program_status_endpoint

    modules = sentio_beta_client.available_modules()
    assert modules, "No available modules"
    modules_started = any(
        module.status in ("IN-PROGRESS", "COMPLETED") for module in modules
    )

    assert not modules_started

    sentio_beta_client.start_goal()
    sentio_beta_client.wait_for_activity_content()


def test_bat_web_017(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    sentio_beta_client.navigate_dashboard()

    in_progress_programs = sentio_beta_client.in_progress_programs()
    assert in_progress_programs, "No in_progress programs available"

    test_program = next(
        p for p in in_progress_programs
        if p.title == sentio_beta_client.programs["mental_health"]
    )

    sentio_beta_client.continue_program(test_program.title)
    assert sentio_beta_client.program_status_endpoint

    sentio_beta_client.continue_goal()
    sentio_beta_client.next_activity()


def test_bat_web_018(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    sentio_beta_client.navigate_dashboard()

    in_progress_programs = sentio_beta_client.in_progress_programs()
    assert in_progress_programs, "No in_progress programs available"

    test_program = next(
        p for p in in_progress_programs
        if p.title == sentio_beta_client.programs["mental_health"]
    )

    sentio_beta_client.continue_program(test_program.title)
    assert sentio_beta_client.program_status_endpoint

    sentio_beta_client.continue_goal()
    sentio_beta_client.complete_goal()


def test_bat_web_019(sentio_beta_client):
    assert sentio_beta_client.program_status_endpoint

    sentio_beta_client.continue_goal()
    # Note: Will not entirely complete goal as the start_exercise() method will force a return and end the test
    sentio_beta_client.complete_goal()

    # BAT-WEB-019 is to test the exercise start only, so assert the URL once the return from complete_goal is received
    assert sentio_beta_client.current_url.endswith("/input")

# TODO: BAT-WEB-020
# TODO: BAT-WEB-021
# TODO: BAT-WEB-022
# TODO: BAT-WEB-023

def test_bat_web_024(sentio_beta_client):
    assert sentio_beta_client._is_authenticated

    header = sentio_beta_client.header
    header_buttons = header.elements["buttons"]

    # 4: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 5: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["menu_sign_out"])
    assert sentio_beta_client.base_url in sentio_beta_client.current_url.lower()

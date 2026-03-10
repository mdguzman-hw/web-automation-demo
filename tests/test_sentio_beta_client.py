################# BUILD ACCEPTANCE ################
############## SENTIO BETA - CLIENT ###############
from selenium.webdriver.common.by import By


# TEST: Navigate Sentio Beta - Client
def test_bat_web_014(sentio_beta_client):
    sentio_beta_client.navigate_landing()
    assert sentio_beta_client.landing_url in sentio_beta_client.current_url.lower()


# TEST: Sentio Beta - Client Login
def test_bat_web_015(sentio_beta_client, quantum, credentials):
    assert sentio_beta_client._is_landing
    elements = sentio_beta_client.landing_elements

    sentio_beta_client.click_element(By.LINK_TEXT, elements["get_started"])
    assert quantum.base_url + "/" + sentio_beta_client.language + "/login" in sentio_beta_client.current_url.lower()

    sentio_beta_client.go_back()
    sentio_beta_client.click_element(By.LINK_TEXT, elements["login"])
    assert quantum.base_url + "/" + sentio_beta_client.language + "/login" in sentio_beta_client.current_url.lower()

    quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert sentio_beta_client.wait_for_dashboard()


# TEST: Start Program
def test_bat_web_016(sentio_beta_client):
    assert sentio_beta_client._is_authenticated

    # 1: Check for In Progress Programs
    in_progress_programs = sentio_beta_client.in_progress_programs()

    # 1.1: Withdraw from In Progress Programs
    for program in in_progress_programs:
        sentio_beta_client.withdraw_program(program)
        assert sentio_beta_client.wait_for_dashboard()

    programs = sentio_beta_client.available_programs()
    assert programs

    completed_status = {
        "en": "Completed",
        "fr": "Exercice terminé"
    }

    # 1.2: Filter programs that are Completed or Not started
    valid_programs = [
        p for p in programs
        if p.status is None or p.status == completed_status[sentio_beta_client.language].upper()
    ]
    assert valid_programs, "No completed or unstarted programs available"

    # Can modify this to be a specific program, if required
    # Pick random program to test
    # test_program = random.choice(valid_programs)

    # 2: Specify program to test
    test_program = next(
        p for p in valid_programs
        if p.title == sentio_beta_client.programs["anxiety"]
    )

    # 3: Navigate to Program Overview
    sentio_beta_client.navigate_overview(test_program.title)
    assert test_program.href in sentio_beta_client.current_url.lower()

    # 3: Navigate to Program Assessment
    sentio_beta_client.navigate_assessment()
    assert "/assessments" and "take" in sentio_beta_client.current_url.lower()

    # 4: Complete Program Assessment
    sentio_beta_client.complete_assessment()
    assert "/assessments" and "results" in sentio_beta_client.current_url.lower()

    # 5: Retrieve Available tiers and provinces for the program
    tiers = sentio_beta_client.available_tiers()
    provinces = sentio_beta_client.available_provinces()
    assert tiers
    assert provinces

    # Can modify to be a specific tier and province, if required
    # Pick random program to test
    # test_tier = random.choice(tiers)
    # test_province = random.choice(provinces)

    # 6: Specify program tier and province
    test_tier = tiers["TIER_2"]
    test_province = provinces["Prince Edward Island"]
    sentio_beta_client.start_program(test_tier, test_province)
    sentio_beta_client.wait_for_activity_content()

    # 7: Navigate to dashboard and ensure test program is now In Progress
    sentio_beta_client.navigate_dashboard()
    assert sentio_beta_client.wait_for_dashboard()
    in_progress_programs = sentio_beta_client.in_progress_programs()
    assert any(
        p.title == test_program.title
        for p in in_progress_programs
    )


# TEST: Continue Program
def test_bat_web_017(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    assert sentio_beta_client.dashboard_endpoint in sentio_beta_client.current_url.lower()
    in_progress_programs = sentio_beta_client.in_progress_programs()
    assert in_progress_programs, "No in progress programs available"

    # Can modify to be a specific program, if required
    # test_program = random.choice(in_progress_programs)

    # 1: Specify program to test
    test_program = next(
        p for p in in_progress_programs
        if p.title == sentio_beta_client.programs["anxiety"]
    )

    # 2: Continue program
    sentio_beta_client.continue_program(test_program.title)
    assert test_program.href_toc in sentio_beta_client.current_url.lower()


# TEST: Start Goal
def test_bat_web_018(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    sentio_beta_client.navigate_dashboard()
    assert sentio_beta_client.wait_for_dashboard()

    # 1: Test: Continue program
    sentio_beta_client.continue_program(sentio_beta_client.programs["anxiety"])
    assert sentio_beta_client.program_status_endpoint

    modules = sentio_beta_client.available_modules()
    assert modules, "No modules found"
    modules_started = any(
        module.status in ("IN-PROGRESS", "COMPLETED") for module in modules
    )
    assert not modules_started

    # 2: Test: Start Goal
    sentio_beta_client.start_goal()
    modules = sentio_beta_client.available_modules()
    in_progress_module = next(
        (m for m in modules if m.status == "IN-PROGRESS"), None
    )

    assert in_progress_module, "No in-progress module found"
    assert in_progress_module.title == sentio_beta_client.current_module


# TEST: Continue Goal
def test_bat_web_019(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    assert sentio_beta_client.program_status_endpoint

    sentio_beta_client.continue_goal()


# TEST: Complete Goal
def test_bat_web_020(sentio_beta_client):
    assert sentio_beta_client._is_authenticated

    sentio_beta_client.complete_goal()
    assert sentio_beta_client.program_status_endpoint

    modules = sentio_beta_client.available_modules()
    completed_module = next(
        (m for m in modules if m.title == sentio_beta_client.current_module), None
    )
    assert completed_module, "Completed module not found"
    assert completed_module.status == "COMPLETED"


# TEST: Complete Program
def test_bat_web_021(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    assert sentio_beta_client.program_status_endpoint

    modules = sentio_beta_client.available_modules()
    while any(module.status != "COMPLETED" for module in modules):
        sentio_beta_client.continue_goal()
        sentio_beta_client.complete_goal()
        modules = sentio_beta_client.available_modules()

    assert all(module.status == "COMPLETED" for module in modules)


# TODO: BAT-WEB-022 | Live Chat

# TEST: Sentio Beta - Client Logout
def test_bat_web_023(sentio_beta_client):
    assert sentio_beta_client._is_authenticated

    header = sentio_beta_client.header
    header_buttons = header.elements["buttons"]

    # 1: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 2: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["menu_sign_out"])
    assert sentio_beta_client.base_url in sentio_beta_client.current_url.lower()

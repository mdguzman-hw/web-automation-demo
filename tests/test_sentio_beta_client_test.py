################# BUILD ACCEPTANCE ################
############## SENTIO BETA - CLIENT ###############
############## v2 ###############
from selenium.webdriver.common.by import By


# TEST: Navigate Sentio Beta - Client
def test_bat_web_012(sentio_beta_client_test):
    sentio_beta_client_test.navigate_landing()
    assert sentio_beta_client_test.landing_url in sentio_beta_client_test.current_url.lower()


# TEST: Sentio Beta - Client Login
def test_bat_web_013(sentio_beta_client_test, quantum, credentials):
    assert sentio_beta_client_test._is_landing
    elements = sentio_beta_client_test.landing_elements

    sentio_beta_client_test.click_element(By.LINK_TEXT, elements["get_started"])
    assert quantum.base_url + "/" + sentio_beta_client_test.language + "/login" in sentio_beta_client_test.current_url.lower()

    sentio_beta_client_test.go_back()
    sentio_beta_client_test.click_element(By.LINK_TEXT, elements["login"])
    assert quantum.base_url + "/" + sentio_beta_client_test.language + "/login" in sentio_beta_client_test.current_url.lower()

    quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert sentio_beta_client_test.wait_for_dashboard()


# TEST: Start Program
def test_bat_web_014(sentio_beta_client_test):
    assert sentio_beta_client_test._is_authenticated

    in_progress_programs = sentio_beta_client_test.in_progress_programs()

    for program in in_progress_programs:
        sentio_beta_client_test.withdraw_program(program)
        assert sentio_beta_client_test.wait_for_dashboard()

    programs = sentio_beta_client_test.available_programs()
    assert programs

    completed_status = {
        "en": "Completed",
        "fr": "Exercice terminé"
    }
    # Filter programs that are Completed or Not started
    valid_programs = [
        p for p in programs
        if p.status is None or p.status == completed_status[sentio_beta_client_test.language].upper()
    ]
    assert valid_programs, "No completed or unstarted programs available"

    # Can modify this to be a specific program, if required
    # Pick random program to test
    # test_program = random.choice(valid_programs)

    # Specify program to test
    test_program = next(
        p for p in valid_programs
        if p.title == sentio_beta_client_test.programs["anxiety"]
    )

    sentio_beta_client_test.navigate_overview(test_program.title)
    assert test_program.href in sentio_beta_client_test.current_url.lower()

    sentio_beta_client_test.navigate_assessment()
    assert "/assessments" and "take" in sentio_beta_client_test.current_url.lower()

    sentio_beta_client_test.complete_assessment()
    assert "/assessments" and "results" in sentio_beta_client_test.current_url.lower()

    tiers = sentio_beta_client_test.available_tiers()
    provinces = sentio_beta_client_test.available_provinces()
    assert tiers
    assert provinces

    # Can modify to be a specific tier and province, if required
    # Pick random program to test
    # test_tier = random.choice(tiers)
    # test_province = random.choice(provinces)

    # Specify program tier and province
    test_tier = tiers["TIER_2"]
    test_province = provinces["Prince Edward Island"]
    sentio_beta_client_test.start_program(test_tier, test_province)
    sentio_beta_client_test.wait_for_activity_content()

    sentio_beta_client_test.navigate_dashboard()
    assert sentio_beta_client_test.wait_for_dashboard()

    in_progress_programs = sentio_beta_client_test.in_progress_programs()
    assert any(
        p.title == test_program.title
        for p in in_progress_programs
    )


# TEST: Continue Program
def test_bat_web_015(sentio_beta_client_test):
    assert sentio_beta_client_test._is_authenticated
    assert sentio_beta_client_test.dashboard_endpoint in sentio_beta_client_test.current_url.lower()
    in_progress_programs = sentio_beta_client_test.in_progress_programs()
    assert in_progress_programs, "No in progress programs available"

    # Can modify to be a specific program, if required
    # test_program = random.choice(in_progress_programs)

    # Specify program to test
    test_program = next(
        p for p in in_progress_programs
        if p.title == sentio_beta_client_test.programs["anxiety"]
    )

    sentio_beta_client_test.continue_program(test_program.title)
    assert test_program.href_toc in sentio_beta_client_test.current_url.lower()


# TEST: Start Goal
def test_bat_web_016(sentio_beta_client_test):
    assert sentio_beta_client_test._is_authenticated
    sentio_beta_client_test.navigate_dashboard()
    assert sentio_beta_client_test.wait_for_dashboard()

    sentio_beta_client_test.continue_program(sentio_beta_client_test.programs["anxiety"])
    assert sentio_beta_client_test.program_status_endpoint

    modules = sentio_beta_client_test.available_modules()
    assert modules, "No modules found"
    modules_started = any(
        module.status in ("IN-PROGRESS", "COMPLETED") for module in modules
    )

    assert not modules_started

    sentio_beta_client_test.start_goal()
    modules = sentio_beta_client_test.available_modules()
    in_progress_module = next(
        (m for m in modules if m.status == "IN-PROGRESS"), None
    )

    assert in_progress_module, "No in-progress module found"
    assert in_progress_module.title == sentio_beta_client_test.current_module

# TEST: Continue Goal
def test_bat_web_017(sentio_beta_client_test):
    assert sentio_beta_client_test._is_authenticated
    assert sentio_beta_client_test.program_status_endpoint

    sentio_beta_client_test.continue_goal()


# TEST: Complete Goal
def test_bat_web_018(sentio_beta_client_test):
    assert sentio_beta_client_test._is_authenticated

    sentio_beta_client_test.complete_goal()
    assert sentio_beta_client_test.program_status_endpoint

    modules = sentio_beta_client_test.available_modules()
    completed_module = next(
        (m for m in modules if m.title == sentio_beta_client_test.current_module), None
    )
    assert completed_module, "Completed module not found"
    assert completed_module.status == "COMPLETED"

# TEST: Complete Program
def test_bat_web_019(sentio_beta_client_test):
    assert sentio_beta_client_test._is_authenticated
    assert sentio_beta_client_test.program_status_endpoint

    modules = sentio_beta_client_test.available_modules()
    while any(module.status != "COMPLETED" for module in modules):
        sentio_beta_client_test.continue_goal()
        print(f"CURRENT GOAL: {sentio_beta_client_test.current_module}")
        sentio_beta_client_test.complete_goal()
        print(f"GOAL COMPLETED: {sentio_beta_client_test.current_module}")
        modules = sentio_beta_client_test.available_modules()

    assert all(module.status == "COMPLETED" for module in modules)

# TEST: Sentio Beta - Client Logout
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


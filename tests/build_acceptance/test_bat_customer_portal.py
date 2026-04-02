# Copyright © 2026 - Homewood Health Inc.

################# BUILD ACCEPTANCE ################
################# CUSTOMER PORTAL #################
from selenium.webdriver.common.by import By


# TEST: Reports validation
def test_bat_web_024(quantum, customer_portal, credentials, env, record_version):
    # 1: Test - Check version
    record_version("Customer Portal", customer_portal.base_url, env)

    # 2: Navigate to Customer Portal - Always EN
    quantum = customer_portal.quantum
    customer_portal.driver.get(customer_portal.base_url)
    assert quantum.base_url in quantum.current_url.lower()

    # 2: Test - Login - Customer Portal - Personal
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert customer_portal.wait_for_portal_login()
    customer_portal.set_authenticated(True)

    # 2.1: Login always navigates to EN, need to toggle to french manually after login
    header = customer_portal.header
    header_buttons = header.elements["buttons"]
    header_dropdown = header.elements["dropdown"]
    if customer_portal.language == "fr":
        header.click_element("css selector", ".btn.btn-nav-item.btn-language.btn-icon-spaced")
        assert "fr" in customer_portal.current_url.lower()

    # 3: Test - Insights
    assert customer_portal.wait_for_tableau_report()

    header.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"dropdown\"]")
    assert header.wait_for_insights_dropdown()
    header.click_element(By.LINK_TEXT, header_dropdown["dropdown_eq"])
    assert customer_portal.wait_for_power_bi_report()

    header.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"dropdown\"]")
    assert header.wait_for_insights_dropdown()
    header.click_element(By.LINK_TEXT, header_dropdown["dropdown_ahs"])
    assert customer_portal.wait_for_power_bi_report()

    # 4: Test - Logout
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    header.click_element(By.CSS_SELECTOR, header_buttons["menu_sign_out"])
    assert header.wait_for_sign_out_group()

    header.click_element(By.LINK_TEXT, header_buttons["menu_sign_out_all"])
    assert quantum.domain in quantum.current_url.lower()

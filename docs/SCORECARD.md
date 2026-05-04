# Codebase Scorecard — web-automation-demo

---

## Score

| | |
|---|---|
| **Previous** | 7.8 / 10 |
| **Current** | 8.1 / 10 |
| **Last reviewed** | 2026-05-03 |

---

## What Improved

| # | Item | Previous | Status |
|---|------|----------|--------|
| 1 | Loading spinner consistency — `loadingPage` invisibility now in all `wait_for_*` methods | Missing from 8 methods | **Fixed** |
| 2 | `is_assessment_complete()` BETA URL pattern — now checks both `pathfinder/assessment` and `recommendation` independently | Would never match BETA URL | **Fixed** |
| 3 | XPath in `continue_booking` — `/p` → `//p` | Silent DOM mismatch | **Fixed** |
| 4 | `wait_for_booking_create` — added `loadingPage` wait and env-specific container (`container-confirm-booking` for BETA) | Wrong container, no spinner wait | **Fixed** |
| 5 | `navigate_toc` intermittent failure — pre-checks `program_status_endpoint` before attempting click | Stale element race condition | **Fixed (workaround)** |
| 6 | Meet Now speedbump in `complete_service_confirm_form` — waits for either `meetnow` or `booking` URL | Missing speedbump path caused timeout | **Fixed** |
| 7 | `InsecureRequestWarning` suppressed via `pytest.ini filterwarnings` | Polluted test output | **Fixed** |
| 8 | Duplicate `test_bat_web_006` function name | Silent test loss | **Fixed** |
| 9 | `test_smoke_homeweb_006` implemented — PulseCheck slider for all 5 feelings with history validation | Stubbed / skipped | **Implemented** |
| 10 | `wait_for_booking_details` — detects `section-error`, prints error text, and skips test cleanly | Would timeout and fail | **Fixed** |
| 11 | `PulseCheck` class extracted — constants live at module level alongside `DashboardTile`, `ProviderTile` | N/A | **New** |
| 12 | Wellness nav added to `HeaderHomeweb` EN/FR (`navigate_wellness()`) | Missing | **New** |
| 13 | `navigate_pulsecheck()` added — navigates via dashboard tile, used in smoke_005 and smoke_006 loop | Inline in test | **Refactored** |
| 14 | Screenshot on failure — `pytest_runtest_makereport` hook captures and saves screenshot to `reports/screenshots/` on any test failure | No screenshot on failure | **New** |
| 15 | LOCAL environment support — `env` fixture expanded to `["prod", "beta", "local"]`; terminal report and CSV now include LOCAL column; test ordering updated | PROD + BETA only | **New** |
| 16 | `Homeweb.go_back()` — hardcoded `"homeweb.ca"` replaced with `self.domain`; would have failed in BETA and LOCAL sessions | Broken in BETA/LOCAL | **Fixed** |
| 17 | `Homeweb.wait_for_dashboard()` — hardcoded `HOMEWEB_DOMAIN` replaced with `self.domain` | Same breakage as above | **Fixed** |
| 18 | `test_bat_homeweb-new.py` — converted from a stub (commented list) to 4 active tests (001–004) with `EXPECTED: \| ACTUAL:` assertion messages | Stub only | **Implemented** |
| 19 | `fresh_1` / `fresh_2` credentials added to `conftest.py` and `.env` for new portal test accounts | Missing | **New** |
| 20 | `test_bat_web_003` — full Standard Registration flow (DSGDEMO, 6 steps) with per-step `record_output`, URL assertions, timestamped unique accounts | Stub | **Implemented** |
| 21 | `test_bat_web_004` — Login with latest registered account read from `registered-accounts.xlsx` | Stub (`FTT_ACCOUNT`) | **Implemented** |
| 22 | `reports/registered-accounts.xlsx` — persistent account tracking spreadsheet written on every `test_bat_web_003` pass; columns: Date, Timestamp, Env, Org, Division, Role, First Name, Last Name, Preferred Name, Email, DOB, Password, Marketing Opt-in | Missing | **New** |
| 23 | `_run_timestamp` — single session-start timestamp shared across report filenames, screenshots, and accounts spreadsheet for easy cross-referencing | Independent timestamps per artifact | **Fixed** |
| 24 | `continue_from_verify()` — dedicated method targeting "Continue" by text to avoid `btn-primary` collision with "Send code" on the verify identity page | Wrong button clicked | **Fixed** |
| 25 | `QuantumAPI` registration methods — full suite: `wait_for_url_path`, `wait_for_org_search/results`, `search_org`, `select_org`, `wait_for_role_selection`, `select_role`, `continue_registration`, `fill_registration_details`, `fill_password_form`, `enter_email_verification_code` | Missing | **New** |
| 26 | `openpyxl==3.1.5` added to `requirements.txt` | Missing | **New** |

---

## Open Issues

| # | Issue | Severity | Notes |
|---|-------|----------|-------|
| 1 | **`PulseCheck.LABELS` English-only** | Medium | `get_latest_pulsecheck_history()` returns DOM text (localized), but `LABELS` only has English. The history validation in `test_smoke_homeweb_006` will fail in a FR session. Related: `smoke_017` has a hardcoded EN `aria-label="Sign In"` that also fails in FR. |
| 2 | **Duplicate `wait_for_resources` definition** | Low | `suites/Homeweb.py` lines 77 and 87 — first definition is dead code, silently overridden. Unremoved across two review cycles. |
| 3 | **Env branching expanding inside page objects** | Medium | `if self.env == "beta"` now spans: `confirm_booking`, `select_booking_options`, `wait_for_booking_create`, `wait_for_booking_digest`, `wait_for_booking_details`, `complete_service_confirm_form`, `ProviderTile.provider_details_link`. LOCAL env adds a third branch path to `Homeweb.__init__` — this pattern will keep growing. |
| 4 | **Unreachable `return True` in `wait_for_booking_details`** | Low | Live `return True` at line 333, followed by a commented-out block that also contains a `return True` at line 351. Dead code that looks like it executes. |
| 5 | **`time.sleep()` workarounds** | Medium | Still present in: `navigate_overview`, `start_program`, `continue_goal`, `select_previous_entry`, `complete_steps`, `next_activity` (SentioClient); `end_services`, `select_provider` (Homeweb); `DashboardTile.navigate`. None replaced with `wait.until` conditions. |
| 6 | **`BasePage.click_element` double DOM lookup** | Medium | Root issue unresolved — two separate `wait.until` calls for the same element create a stale-element window between lookup and click. |
| 7 | **`phone` variable reused for comments field** | Low | `complete_booking_create_form`: `phone = self.wait.until(...(By.ID, "comments"))`. Misleading variable name. |
| 8 | **Dead and commented-out code volume growing** | Low | `test_bat_homeweb-new.py` now has 19 commented-out test bodies (~490 lines). This is intentional WIP staging, but combined with `Homeweb.py` dead code (`select_provider_time`, `choose_confirmation_method`, old `wait_for_resources`, debug prints, stale TODOs) the signal-to-noise ratio is declining. |
| 9 | **`pre_url` dead variable in `wait_for_next_step`** | Low | `pre_url = self.current_url` is assigned on entry but never read. Unresolved across two review cycles. |
| 10 | **`SentioClient.__init__` env branch is inert** | Low | Both `if env == "prod"` and `else` branches assign the same `SENTIO_BETA_CLIENT_*` constants. The conditional has never done anything. |
| 11 | **`registered-accounts.xlsx` Onboarded column not yet populated** | Medium | Column exists in headers but no value is written — requires a post-login API call to `{base_url}/app/{language}/ajax/homeweb/client` to read the 5 `showOnboarding*` flags and update the last row. |
| 12 | **`test_bat_web_003` email verification requires manual input** | Medium | Step 5 uses `input()` to pause for manual code entry. TODO: wire in via IMAP/email API to make fully automated. |
| 13 | **`test_bat_web_003` password is hardcoded** | Low | `password = "QuantumSentio123$"` is inline in the test rather than sourced from `.env`. |

---

## Recommendations

| Priority | Action |
|----------|--------|
| High | Fix `BasePage.click_element` — single `wait.until(element_to_be_clickable)` call to eliminate the stale-element window |
| High | Add `PulseCheck.LABELS` FR entries and fix `smoke_017` hardcoded EN `aria-label` — required before FR session coverage is meaningful |
| Medium | Replace `time.sleep()` with `wait.until` conditions in `select_provider`, `end_services`, `DashboardTile.navigate`, and SentioClient scroll/submit methods |
| Medium | Evaluate BETA subclass or strategy to stop `if self.env` branching from growing further in page methods — LOCAL env makes this more urgent |
| High | Implement post-login `get_client_data()` call in `test_bat_web_004` to populate Onboarded column in `registered-accounts.xlsx` |
| Medium | Move hardcoded registration password to `.env` |
| Medium | Wire email verification code retrieval via IMAP/email API to remove `input()` pause from `test_bat_web_003` |
| Low | Remove first `wait_for_resources` definition (line 77 in `Homeweb.py`) |
| Low | Remove `pre_url` dead variable from `wait_for_next_step` |
| Low | Fix or remove `SentioClient.__init__` env conditional — assign correct PROD constants or remove the branch entirely |
| Low | Rename `phone` → `comments` in `complete_booking_create_form` |
| Low | Audit and remove dead code in `Homeweb.py`: `select_provider_time`, `choose_confirmation_method`, the unreachable `return True`, debug `print` statements, and stale TODO comments |

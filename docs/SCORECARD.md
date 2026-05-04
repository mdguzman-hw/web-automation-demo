# Codebase Scorecard — web-automation-demo

---

## Score

| | |
|---|---|
| **Previous** | 8.7 / 10 |
| **Current** | 8.8 / 10 |
| **Last reviewed** | 2026-05-04 |

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
| 27 | `Homeweb.logout()` — encapsulates open-menu → sign-out → wait-for-logout → navigate-landing; `test_bat_web_013` reduced to 2 lines | Inline in every test | **Refactored** |
| 28 | `BasePage.take_screenshot(name, logger=None)` — centralised screenshot saving with auto timestamp + date folder; `import os` and `_run_timestamp` removed from test files | Copy-pasted in each test | **Refactored** |
| 29 | `Homeweb.navigate_sign_in()` — encapsulates ANON header click + URL assertion; raw `click_element` + `assert paths["sign_in"]` pairs removed from all callers | Repeated inline | **Refactored** |
| 30 | `Homeweb.navigate_landing()` — domain assertion baked in; callers no longer repeat `assert homeweb.domain in current_url` | Repeated inline | **Refactored** |
| 31 | `Homeweb.navigate_dashboard()` — `wait_for_dashboard()` baked in; all `navigate_dashboard()` + `assert wait_for_dashboard()` pairs removed across `test_bat_homeweb.py`, `test_bat_homeweb-new.py`, `test_smoke_homeweb.py`, and `Homeweb.navigate_pulsecheck` | Repeated inline across 3 files | **Refactored** |
| 32 | `Homeweb.navigate_scn_assessment()` — encapsulates SCN tile click + `wait_for_assessment()` assertion | Inline in test | **Refactored** |
| 33 | SCN scenario numbering corrected to match new portal (1: Resource ONLY, 2: Prof+Sentio, 3: Prof ONLY, 4: Sentio ONLY, 5: Legal, 6: Financial); all callers in both test files updated | Old 1–4 numbering inconsistent with new suite | **Fixed** |
| 34 | `assert_recommendation_scenario_5/6` implemented — `_assert_recommendation_row()` validates 2-column row (Prof Support tile + resource list) with fallback to resource-only tile | `NotImplementedError` stubs | **Implemented** |
| 35 | `scripts/test_scn.sh` — one-command runner for SCN suite (BAT-WEB-014–020) against beta | No dedicated runner | **New** |
| 36 | `test_bat_homeweb-new.py` expanded from 4 to 21 active tests covering Registration, Login, Library, Kickouts, Course Consent, Logout, and all 6 SCN scenarios | 4 active tests | **Implemented** |
| 37 | Reports directory restructured — each run now gets its own subdirectory `reports/{date}/{timestamp}/`; timestamp moved to filename prefix on CSV/TXT/scenario files; `_reports_dir` computed once at module level in `conftest.py` | All files flat in date folder, timestamp suffix | **Improved** |
| 38 | `search_and_open_resource` — replaced `StaleElementReferenceException` retry with `wait.until(visibility_of_element_located)` + `click_element(*locator)`; eliminates intermediate list collection entirely | Stale element retry loop | **Fixed** |
| 39 | `StaleElementReferenceException` promoted to top-level import in `Homeweb.py`; inline local imports removed; city dropdown usage flagged with TODO for JS atomic replacement | Local inline imports | **Cleaned** |
| 40 | `test_bat_web_003` — interactive prompt at test start: `Include new registration in this run? (y/n)`; skips cleanly if user declines | Hardcoded `pytest.skip` | **Improved** |
| 41 | CSV and TXT report files removed — `_write_test_matrix_xlsx` is now the single report artifact per run | Three separate output files | **Consolidated** |
| 42 | Matrix format: columns ID, Description, Logs, PROD/BETA/LOCAL; TOTALS section includes Build (versions), Passed, Failed, Not Run, Completed, Percentage Passed | Separate CSV for metrics | **New** |
| 43 | `pytest_collection_finish` hook — parses `# BAT-WEB-XXX \| Description` comments above each test function to build `_test_metadata`; drives matrix row population | No automatic test metadata | **New** |
| 44 | Failure detail appended to Logs cell — last meaningful assertion line from longrepr shown as `[ENV FAILED] ...` so failures are self-contained in the matrix | Lost on TXT removal | **New** |
| 45 | Logs column defaults to `-` when no `record_output` stdout is captured | Empty cell | **Fixed** |
| 46 | Run time sourced from `terminalreporter._sessionduration` (pytest's own timer) and displayed in terminal summary | Not tracked | **New** |
| 47 | Terminal summary path shortened to `/date/timestamp/file`; label changed from "Matrix saved" to "Report saved" | Full absolute path | **Improved** |
| 48 | `test_bat_homeweb.py` — all 23 `# TEST:` comments updated to `# BAT-WEB-XXX \| description` format; report now generates for the old portal suite | No report generated | **Fixed** |
| 49 | `select_booking_options` — "Review & confirm" button selector replaced with XPath text match `//button[contains(normalize-space(), 'Review') and not(contains(@class, 'disabled'))]`; resilient to CSS class changes in new portal UI | `btn-primary` hardcoded class broke on PROD new portal | **Fixed** |
| 50 | Terminal summary cleanup — `total_completed` dead variable removed; version strings inlined into `if _versions:` block; `run_time` computation moved before output block | Minor dead code | **Cleaned** |

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
| 14 | **`navigate_messages()` used `By.CLASS_NAME` for `managerMessages`** | Low | Should be `By.ID` — caused `test_bat_web_021` to timeout. Fixed by user. |
| 15 | **`StaleElementReferenceException` still used in city dropdown** | Low | City reload check in `Homeweb.py` still uses try/except on stale element. TODO to replace with JS atomic read once backwards compatibility confirmed. |
| 16 | **TODO: Investigate PROD booking selectors against new portal UI** | Medium | `btn-primary` button selector fixed; time slot and modality selectors in `select_booking_options` PROD branch may also diverge as new portal rolls out to PROD. |

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

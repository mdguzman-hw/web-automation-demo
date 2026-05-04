# SUMMARY.md

## Web Automation Demo — Project Summary
Copyright © 2026 - Homewood Health Inc.

---

## Overview

This is a **Selenium + pytest** web automation framework built to test Homewood Health's suite of web applications. It uses the **Page Object Model (POM)** pattern and supports multi-environment test execution across **PROD**, **BETA**, and **LOCAL** environments from a single test file.

---

## Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.14 | Language |
| pytest | 8.3.4 | Test runner |
| Selenium | 4.40.0 | Browser automation |
| webdriver-manager | 4.0.2 | ChromeDriver management |
| python-dotenv | 1.2.1 | Environment variable loading |
| openpyxl | 3.1.5 | Excel account tracking spreadsheet |
| Chrome (Incognito) | — | Browser (headless-capable) |

---

## Applications Under Test

| App | PROD URL | BETA URL | Notes |
|-----|----------|----------|-------|
| Homeweb | homeweb.ca | beta.homeweb.ca | Employee mental health portal |
| Quantum API | api.homewoodhealth.io | betaapi.homewoodhealth.io | Authentication backend |
| Customer Portal | portal.homewoodhealth.com | — | PROD only |
| Sentio Client | — | beta.sentioapp.com | iCBT platform (BETA only) |
| Sentio Provider | — | beta-portal.sentioapp.com | Provider portal (BETA only) |

---

## Project Structure

```
web-automation-demo/
├── conftest.py               # Fixtures, hooks, reporting, CLI options
├── pytest.ini                # pytest config and markers
├── requirements.txt          # Python dependencies
├── .env                      # Credentials (not committed)
│
├── core/
│   ├── BasePage.py           # Base class with Selenium helpers
│   ├── Constants.py          # URL and domain constants
│   ├── Header.py             # Header components for all apps
│   ├── Login.py              # Quantum API login page locators
│   └── Public.py             # Anonymous/public page locators
│
├── suites/
│   ├── Homeweb.py            # Homeweb page object (~1100 lines)
│   ├── QuantumAPI.py         # Auth/login page object
│   ├── CustomerPortal.py     # Customer portal page object
│   ├── SentioClient.py       # Sentio client page object
│   └── SentioProvider.py     # Sentio provider page object
│
├── tests/
│   ├── build_acceptance/
│   │   ├── test_bat_homeweb.py       # BAT — Original Homeweb portal (23 tests)
│   │   ├── test_bat_homeweb-new.py   # BAT — New portal / Beta (WIP, 4 active)
│   │   ├── test_bat_web.py           # BAT — General web tests
│   │   ├── test_bat_customer_portal.py
│   │   ├── test_bat_sentio_client.py
│   │   └── test_bat_sentio_provider.py
│   └── smoke/
│       ├── test_smoke_homeweb.py     # Smoke — Homeweb (tests 003–039)
│       └── test_smoke_web.py         # Smoke — General web
│
├── reports/                  # Auto-generated CSV + TXT reports per run
└── docs/
    ├── CONFIG.md             # Environment config & execution guide
    ├── SCORECARD.md          # Test scorecard
    └── SUMMARY.md            # This file
```

---

## Architecture

### Page Object Model

- **`BasePage`** — shared base class providing `click_element()` with scroll-into-view, stability wait, and clickability guard.
- **Suite classes** (e.g., `Homeweb`, `QuantumAPI`) extend `BasePage` and encapsulate all locators and page actions.
- **`Header`** — a unified header class that maps to the correct locator set based on `domain` + `user` (AUTH/ANON) + `language` (EN/FR).
- **Page locators** (`Login`, `Public`, `Header*`) use language-keyed dictionaries (`EN`, `FR`) for bilingual support.

### Multi-Environment Parametrization

The `env` fixture in `conftest.py` parametrizes every test across `prod`, `beta`, and `local`:

```bash
pytest tests/build_acceptance/test_bat_homeweb.py           # All environments
pytest tests/build_acceptance/test_bat_homeweb.py --env=prod  # PROD only
pytest tests/build_acceptance/test_bat_homeweb.py --env=beta  # BETA only
```

Test IDs appear as: `test_bat_web_001[PROD]`, `test_bat_web_001[BETA]`, `test_bat_web_001[LOCAL]`

### Test Ordering

`pytest_collection_modifyitems` sorts collected tests by:
1. Environment priority: PROD (0) → BETA (1) → LOCAL (2)
2. Test number: 001 → 002 → ...

This ensures all PROD tests complete before BETA tests begin, avoiding cross-environment session contamination.

---

## Test Suites

### Build Acceptance Tests (BAT)

Full end-to-end flows run per build to confirm core functionality.

| Test ID | Description |
|---------|-------------|
| BAT-WEB-001 | Navigate to Homeweb landing, record versions |
| BAT-WEB-002 | Verify landing page articles (dynamic + static) |
| BAT-WEB-003 | Login flow via Quantum API |
| BAT-WEB-004 | Navigate to a specific resource |
| BAT-WEB-005 | Dashboard tiles + Sentio kickout |
| BAT-WEB-006 | Pathfinder — Scenario 4 (Resource only) |
| BAT-WEB-007 | Logout |
| BAT-WEB-008 | Login with second account |
| BAT-WEB-009 | Kickouts: Childcare, Eldercare, HRA (PROD only) |
| BAT-WEB-010 | Course consent modal |
| BAT-WEB-011 | Cancel active services |
| BAT-WEB-012 | Live Chat (manual — skipped) |
| BAT-WEB-013 | Pathfinder — Scenario 1 (Professional Support + Sentio iCBT) |
| BAT-WEB-014 | Pathfinder — Scenario 2 (Sentio iCBT only, manual) |
| BAT-WEB-015 | Pathfinder — Scenario 3 (Professional Support only) |
| BAT-WEB-016 | Create Pathfinder booking |
| BAT-WEB-017 | Complete Pathfinder booking |
| BAT-WEB-018 | Pathfinder — Scenario 5 (Legal + Financial flows) |
| BAT-WEB-019 | Resource Library — initial state |
| BAT-WEB-020 | Resource Library — primary category navigation |
| BAT-WEB-021 | Resource Library — subcategory navigation |
| BAT-WEB-022 | Resource search |
| BAT-WEB-023 | Embedded mobile resources |

### Smoke Tests

Lightweight checks that confirm critical paths are functional.

| Test ID | Description |
|---------|-------------|
| SMOKE-003 | Landing page — initial state |
| SMOKE-004 | Dashboard — login and verify |
| SMOKE-005 | PulseCheck — navigate from dashboard |
| SMOKE-006 | PulseCheck — all 5 feelings, validate history |
| SMOKE-007 | Pathfinder — navigate and cancel active services |
| SMOKE-009 | Assessment — complete |
| SMOKE-010 | 5-star rating page (PROD only) |
| SMOKE-011 | Intake / booking create form |
| SMOKE-012 | Booking calendar — select provider and confirm |
| SMOKE-016 | End services + logout |
| SMOKE-017 | Enbridge custom landing + login |
| SMOKE-018 | Suncor custom landing |
| SMOKE-019 | LSO (MAP) custom landing |
| SMOKE-020 | EQ custom landing |
| SMOKE-021 | Alumni custom landing |
| SMOKE-022 | Pacific Blue Cross custom landing |
| SMOKE-023 | External redirects (authenticated) |
| SMOKE-039 | Logout |

### New Portal BAT (`test_bat_homeweb-new.py`)

A parallel BAT suite for the redesigned Homeweb portal (Beta). 21 active tests covering the flows listed below.

| Test ID | Description |
|---------|-------------|
| BAT-WEB-001 | Navigate to Homeweb landing, record versions |
| BAT-WEB-002 | Verify landing page articles (dynamic + static) |
| BAT-WEB-003 | Standard Registration — DSGDEMO (6 steps, timestamped account, writes to `registered-accounts.xlsx`) |
| BAT-WEB-004 | Login with latest account from `registered-accounts.xlsx` |
| BAT-WEB-005 | Navigate to a specific resource |
| BAT-WEB-006 | Resource Library — initial state, log categories |
| BAT-WEB-007 | Resource Library — primary category navigation |
| BAT-WEB-008 | Resource Library — subcategory navigation |
| BAT-WEB-009 | Resource search |
| BAT-WEB-010 | Kickouts: Childcare, Eldercare, HRA |
| BAT-WEB-011 | Sentio kickout via resource search |
| BAT-WEB-012 | Course consent modal |
| BAT-WEB-013 | Logout |
| BAT-WEB-014 | Login — HHI account |
| BAT-WEB-015 | SCN — Scenario 1: Resource ONLY |
| BAT-WEB-016 | SCN — Scenario 2: Professional Support & Sentio |
| BAT-WEB-017 | SCN — Scenario 3: Professional Support ONLY |
| BAT-WEB-018 | SCN — Scenario 4: Sentio ONLY |
| BAT-WEB-019 | SCN — Scenario 5: Legal Flow |
| BAT-WEB-020 | SCN — Scenario 6: Financial Flow |
| BAT-WEB-021 | Messages — navigate and verify inbox |
| BAT-WEB-022 | Embedded mobile resources |

**Module status:**

| Module | Status | Notes |
|--------|--------|-------|
| Registration | [HOLD] | Standard/DSGDEMO done; MFA, Custom, Eligibility List, Additional Fields, Invite Code pending |
| Login | [DONE] | DSGDEMO + HHI |
| Dashboard | [NEXT] | S1 (onboarding TODO), S2, S3 |
| Discover | [NEXT] | Mental Health, Wellness, Work-Life |
| Journey | [NEXT] | Plans, Sessions, Appointments |
| Smart Care Navigation | [DONE] | All 6 scenarios |
| Booking | [NEXT] | — |
| Profile | [NEXT] | — |
| Library | [DONE] | Resource Library, Primary Category, Subcategory |
| Messages | [DONE] | — |

---

## Reporting

After every run, `conftest.py` auto-generates a single Excel report under `reports/MM-DD-YYYY/<timestamp>/`:

- **`<timestamp>_<suite>_matrix.xlsx`** — Full test matrix with per-test results, logs, and totals
- **`fail-<test>-<env>_<timestamp>.png`** — Screenshot saved automatically on any test failure
- **`<timestamp>_<name>.png`** — Manual screenshots taken mid-test (e.g. SCN scenario results)

Each run gets its own subdirectory named after `_run_timestamp`, keeping all artifacts from the same session grouped together.

### Matrix format

| Column | Content |
|--------|---------|
| ID | Test ID (e.g. `BAT-WEB-001`) — parsed from `# BAT-WEB-XXX \| Description` comment above each test |
| Description | Test description from the same comment |
| Logs | `record_output` stdout; failure detail appended as `[ENV FAILED] ...`; `-` if empty |
| PROD / BETA / LOCAL | `Y` (green) / `N` (red) / `-` per environment |

TOTALS section at the bottom: env labels + Build (version info), then Passed, Failed, Not Run, Completed, Percentage Passed per env column.

A formatted summary table is also printed to the terminal:

```
Metric                              PROD    BETA   LOCAL
--------------------------------------------------------------
Passed                                12       8       0
Failed                                 0       1       0
Not Run (Skipped, N/A, etc.)           3       3      23
Completed                             12       9       0
Percentage Passed                    100%     89%     N/A
--------------------------------------------------------------
Total Passed                             20
...
Run Time                             4m 39s

  Report saved: /05-04-2026/20260504_140112/20260504_140112_bat_homeweb-new_matrix.xlsx
```

### Account Tracking

`reports/registered-accounts.xlsx` is a persistent spreadsheet updated every time `test_bat_web_003` passes. Columns:

| Date | Timestamp | Env | Org | Division | Role | First Name | Last Name | Preferred Name | Email | DOB | Password | Marketing Opt-in |
|------|-----------|-----|-----|----------|------|-----------|----------|----------------|-------|-----|----------|-----------------|

The Timestamp column matches the report filename timestamp for easy cross-referencing.

---

## Credentials

All credentials are loaded from `.env` via `python-dotenv`. The following accounts are configured:

| Key | Purpose |
|-----|---------|
| `personal` | Primary test account (HHI employee) |
| `dsg_demo` | DSG demo account |
| `sentio` | Sentio iCBT account (BETA) |
| `hhi_demo` | HHI demo account |
| `lso_test` | LSO / Enbridge test account |
| `fresh_1` | Fresh account #1 (new portal) |
| `fresh_2` | Fresh account #2 (new portal) |

---

## Known Issues & Notes

- **KNOWN ISSUE 1**: Logout always redirects to the EN landing page, regardless of session language. Workaround: manually call `navigate_landing()` after logout.
- **BETA**: Customer Portal, Kickouts (BAT-009), and the 5-star rating page are skipped in beta.
- **PROD**: Sentio Client and Sentio Provider fixtures are skipped in prod.
- There is a duplicate `wait_for_resources` definition in `suites/Homeweb.py` (lines 77 and 87) — the second definition silently overrides the first.
- `test_bat_web_013` has a hardcoded `pytest.skip()` mid-test after clearing services — the assessment flow after that point is not currently exercised automatically.

---

## Running the Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run full BAT suite (all environments)
pytest tests/build_acceptance/test_bat_homeweb.py

# Run smoke suite against PROD only
pytest tests/smoke/test_smoke_homeweb.py --env=prod

# Run new portal BAT against BETA only
pytest tests/build_acceptance/test_bat_homeweb-new.py --env=beta

# Run with custom language
LANGUAGE=fr pytest tests/build_acceptance/test_bat_homeweb.py --env=prod
```

---

*Last updated: 2026-05-04 (reporting consolidated into matrix; test_bat_homeweb.py BAT comments added; booking selector hardened)*

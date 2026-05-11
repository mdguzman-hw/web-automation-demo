# CONFIG.md

## Pytest Environment Configuration & Execution Guide
Copyright © 2026 - Homewood Health Inc.

---

## Overview

This configuration enables:

- Running the same tests against multiple environments (`prod`, `beta`)
- Executing all **PROD tests first**, followed by **BETA tests**
- Eliminating duplicate test files
- Controlling test execution via CLI flags

---

## 1. CLI Configuration (`pytest_addoption`)

### Purpose

Adds custom command-line arguments to control which environment(s) to run and whether to run headed.

---

### Implementation (add to `conftest.py`)

```python
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help="Environment: prod | beta | staging | local | all"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Chrome in headed (visible) mode instead of headless"
    )
```

---

### Usage

```bash
pytest --env=prod
pytest --env=beta
pytest --env=staging
pytest --env=local
pytest --env=all
pytest --env=prod --headed
```

---

### Behavior

| Command          | Result                              |
|------------------|-------------------------------------|
| `--env=prod`    | Run only PROD tests                 |
| `--env=beta`    | Run only BETA tests                 |
| `--env=staging` | Run only STAGING tests              |
| `--env=local`   | Run only LOCAL tests                |
| `--env=all`     | Run all environments                |
| `--headed`      | Launch Chrome in visible window     |

---

### Language

Language is controlled via the `LANGUAGE` environment variable (defaults to `en`):

```bash
# English (default)
pytest tests/build_acceptance/test_bat_homeweb.py --env=prod

# French
LANGUAGE=fr pytest tests/build_acceptance/test_bat_homeweb.py --env=prod

# Both EN and FR in one command (FR runs regardless of EN result)
pytest tests/build_acceptance/test_bat_homeweb.py --env=prod ; LANGUAGE=fr pytest tests/build_acceptance/test_bat_homeweb.py --env=prod
```

---

### Accessing the Value

```python
env_flag = request.config.getoption("--env")
```

---

## 2. Environment Fixture (Parametrization)

### Purpose

Runs the same test suite across multiple environments without duplicating test files.

---

### Implementation

```python
import pytest

@pytest.fixture(params=["prod", "beta", "staging", "local"], ids=["PROD", "BETA", "STAGING", "LOCAL"], scope="session")
def env(request):
    env_flag = request.config.getoption("--env")

    if env_flag != "all" and request.param != env_flag:
        pytest.skip(f"Skipping {request.param} environment")

    return request.param
```

---

### Key Concepts

- `params=["prod", "beta", "staging", "local"]` → runs each test for all environments
- `ids=["PROD", "BETA", "STAGING", "LOCAL"]` → controls output labels
- `request.param` → current environment value
- `pytest.skip(...)` → skips unwanted environments based on CLI
- `instance.env` → attaches environment metadata to the object

---

## 3. Test Ordering (`pytest_collection_modifyitems`)

### Purpose

Ensures all PROD tests run before BETA tests while preserving numeric test order.

---

### Implementation

```python
def pytest_collection_modifyitems(items):
    def get_group(item):
        name = item.name

        import re
        match = re.search(r"test_bat_web_(\d+)", name)
        order = int(match.group(1)) if match else 999

        if "[PROD]" in name:
            env = 0
        elif "[BETA]" in name:
            env = 1
        elif "_beta" in name.lower():
            env = 1
        else:
            env = 2

        return (env, order)

    items.sort(key=get_group)
```

---

### Sorting Logic

Tests are sorted by:

1. Environment (PROD → BETA → STAGING → LOCAL → other)
2. Test number (001 → 002 → ...)

---

### Before Ordering

```
test_001[PROD]
test_001[BETA]
test_002[PROD]
test_002[BETA]
```

---

### After Ordering

```
test_001[PROD]
test_002[PROD]
...

test_001[BETA]
test_002[BETA]
...
```

---

## 4. Before vs After

### Before (Duplicate Tests)

```
test_homeweb.py
test_homeweb_beta.py
```

Problems:

- duplicated logic
- manual `_beta` naming
- harder to maintain

---

### After (Parametrized Tests)

```
test_homeweb.py
```

Output:

```
test_bat_web_001[PROD]
test_bat_web_001[BETA]
```

---

## 5. Fixture Scope Considerations

### Current

```python
scope="session"
```

### Behavior

- browser reused
- cookies persist
- shared session state

### Risks

- PROD → BETA contamination
- session leakage

---

### Safer Alternative

```python
scope="function"
```

| Scope     | Speed | Isolation |
|----------|------|----------|
| session  | fast | low      |
| function | slow | high     |

---

## 6. Execution Flow

```
pytest starts
    ↓
pytest_addoption defines CLI options
    ↓
fixtures parametrize tests (prod + beta)
    ↓
pytest collects tests
    ↓
pytest_collection_modifyitems reorders tests
    ↓
tests execute in controlled order
```

---

## TLDR

- `pytest_addoption` → CLI control (`--env`, `--headed`)
- parametrized `env` fixture → multi-environment testing across PROD/BETA/STAGING/LOCAL
- `pytest_collection_modifyitems` → execution ordering (PROD first, LOCAL last)
- `LANGUAGE=fr` env var → bilingual test execution (EN default)
- Single test file per suite — no duplication


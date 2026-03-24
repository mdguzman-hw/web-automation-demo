# CONFIG.md

## Pytest Environment Configuration & Execution Guide

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

Adds a custom command-line argument to control which environment(s) to run.

---

### Implementation (add to `conftest.py`)

```python
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help="Environment: prod | beta | all"
    )
```

---

### Usage

```bash
pytest --env=prod
pytest --env=beta
pytest --env=all
```

---

### Behavior

| Command        | Result                    |
|----------------|---------------------------|
| `--env=prod`  | Run only PROD tests       |
| `--env=beta`  | Run only BETA tests       |
| `--env=all`   | Run both PROD and BETA    |

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

@pytest.fixture(params=["prod", "beta"], ids=["PROD", "BETA"], scope="session")
def homeweb(request, driver, language):
    env_flag = request.config.getoption("--env")

    if env_flag != "all" and request.param != env_flag:
        pytest.skip(f"Skipping {request.param} environment")

    if request.param == "prod":
        instance = Homeweb(driver, language)
    else:
        instance = HomewebBeta(driver, language)

    instance.env = request.param
    return instance
```

---

### Key Concepts

- `params=["prod", "beta"]` → runs each test for both environments
- `ids=["PROD", "BETA"]` → controls output labels
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

1. Environment (PROD → BETA → other)
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

- `pytest_addoption` → CLI control
- parametrized fixture → multi-environment testing
- `pytest_collection_modifyitems` → execution ordering
- remove duplicated test files

---

## Recommended Next Steps

- remove `_beta` duplicate tests
- apply pattern across all suites
- consider stateless tests for parallel execution


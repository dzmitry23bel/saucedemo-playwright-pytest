# SauceDemo Test Automation Framework

[![Tests](https://github.com/YOUR_GITHUB_USERNAME/saucedemo-playwright-pytest/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/saucedemo-playwright-pytest/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Playwright](https://img.shields.io/badge/playwright-1.47-green)

End-to-end UI test suite for [saucedemo.com](https://www.saucedemo.com) — a demo
e-commerce site built by Sauce Labs specifically for test-automation practice.

Built with **Python, Playwright and pytest**, using the **Page Object Model**
pattern. Covers login, inventory, cart and checkout flows, including negative
and data-driven scenarios.

## Project structure

```
saucedemo-playwright-pytest/
├── pages/                  # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py         # fixtures: login_page, logged_in_page, cart_with_item, ...
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── data/
│   └── users.py            # test user accounts (standard/locked_out/problem/...)
├── .github/workflows/tests.yml
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Running tests

```bash
# all tests, headless
pytest

# headed, in a specific browser
pytest --headed --browser firefox

# only smoke tests
pytest -m smoke

# HTML report
pytest --html=report.html --self-contained-html
```

## Design notes

- **Page Object Model** — every page exposes locators and behavior as methods;
  tests only call methods, never touch selectors directly. Page methods return
  the next `Page` object, so flows read like `login_page.login(...).add_item_to_cart(...).open_cart().checkout()`.
- **pytest-playwright** provides the `page`/`browser`/`base_url` fixtures and
  CLI flags (`--browser`, `--headed`, `--slowmo`, tracing), so no custom
  browser bootstrap code is needed.
- **Fixtures over setup code** — `conftest.py` composes small fixtures
  (`login_page` → `logged_in_page` → `cart_with_item` → `checkout_page_with_item`)
  so each test only asks for the state it needs.
- **Data-driven tests** via `pytest.mark.parametrize` for sort orders, invalid
  credentials, and required-field validation.
- **Markers** (`smoke`, `regression`) let CI or a developer run a fast subset.

## CI

GitHub Actions runs the full suite on every push/PR against `main`
(`.github/workflows/tests.yml`), publishing the HTML report and Playwright
traces as build artifacts.

## Test accounts used

| Username                  | Purpose                              |
|----------------------------|---------------------------------------|
| `standard_user`            | happy-path flows                      |
| `locked_out_user`          | blocked-login negative test           |
| `problem_user`             | available for UI-bug exploration      |
| `performance_glitch_user`  | available for latency-sensitive tests |

All accounts share the password `secret_sauce`, as documented on the SauceDemo
login page itself.

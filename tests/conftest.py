import allure
import pytest

from data.users import STANDARD_USER
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            allure.attach(
                page.screenshot(),
                name="screenshot-on-failure",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture
def login_page(page, base_url):
    page.goto(base_url)
    return LoginPage(page)


@pytest.fixture
def logged_in_page(login_page) -> InventoryPage:
    return login_page.login(STANDARD_USER.username, STANDARD_USER.password)


@pytest.fixture
def cart_with_item(logged_in_page) -> CartPage:
    logged_in_page.add_item_to_cart("Sauce Labs Backpack")
    return logged_in_page.open_cart()


@pytest.fixture
def checkout_page_with_item(cart_with_item) -> CheckoutStepOnePage:
    return cart_with_item.checkout()

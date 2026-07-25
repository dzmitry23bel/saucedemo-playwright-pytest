import allure
import pytest

from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.feature("Inventory")


@allure.title("Inventory page lists all six products")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_inventory_shows_six_products(logged_in_page):
    assert logged_in_page.inventory_items.count() == 6


@allure.title("Adding and removing an item updates the cart badge")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_add_and_remove_item_updates_cart_badge(logged_in_page):
    item = "Sauce Labs Backpack"

    assert logged_in_page.get_cart_count() == 0

    logged_in_page.add_item_to_cart(item)
    assert logged_in_page.get_cart_count() == 1

    logged_in_page.remove_item_from_cart(item)
    assert logged_in_page.get_cart_count() == 0


@allure.title("Multiple items can be added to the cart at once")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_add_multiple_items_to_cart(logged_in_page):
    items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]

    for item in items:
        logged_in_page.add_item_to_cart(item)

    assert logged_in_page.get_cart_count() == len(items)


@allure.story("Sorting")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
@pytest.mark.parametrize(
    "sort_option, expected_order",
    [
        (InventoryPage.SORT_NAME_A_TO_Z, "asc"),
        (InventoryPage.SORT_NAME_Z_TO_A, "desc"),
    ],
)
def test_sort_products_by_name(logged_in_page, sort_option, expected_order):
    logged_in_page.sort_by(sort_option)
    names = logged_in_page.get_product_names()

    assert names == sorted(names, reverse=(expected_order == "desc"))


@allure.story("Sorting")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
@pytest.mark.parametrize(
    "sort_option, reverse",
    [
        (InventoryPage.SORT_PRICE_LOW_TO_HIGH, False),
        (InventoryPage.SORT_PRICE_HIGH_TO_LOW, True),
    ],
)
def test_sort_products_by_price(logged_in_page, sort_option, reverse):
    logged_in_page.sort_by(sort_option)
    prices = logged_in_page.get_product_prices()

    assert prices == sorted(prices, reverse=reverse)

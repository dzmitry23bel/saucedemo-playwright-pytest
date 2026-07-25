import allure
import pytest

pytestmark = pytest.mark.feature("Cart")


@allure.title("Cart page shows the item that was added")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_cart_shows_added_item(cart_with_item):
    assert cart_with_item.get_item_names() == ["Sauce Labs Backpack"]


@allure.title("Item can be removed from the cart page")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_remove_item_from_cart_page(cart_with_item):
    cart_with_item.remove_item("Sauce Labs Backpack")

    assert cart_with_item.get_item_names() == []


@allure.title("Continue shopping returns to inventory and keeps the cart")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_continue_shopping_returns_to_inventory(cart_with_item):
    inventory_page = cart_with_item.continue_shopping()

    assert inventory_page.is_loaded()
    assert inventory_page.get_cart_count() == 1

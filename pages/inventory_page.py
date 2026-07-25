from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = "/inventory.html"

    SORT_NAME_A_TO_Z = "az"
    SORT_NAME_Z_TO_A = "za"
    SORT_PRICE_LOW_TO_HIGH = "lohi"
    SORT_PRICE_HIGH_TO_LOW = "hilo"

    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_items = page.locator(".inventory_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator(".product_sort_container")
        self.burger_menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def is_loaded(self) -> bool:
        return self.page.locator(".inventory_list").is_visible()

    def _add_to_cart_button(self, item_name: str):
        slug = item_name.lower().replace(" ", "-").replace("'", "")
        return self.page.locator(f"#add-to-cart-{slug}")

    def _remove_button(self, item_name: str):
        slug = item_name.lower().replace(" ", "-").replace("'", "")
        return self.page.locator(f"#remove-{slug}")

    def add_item_to_cart(self, item_name: str) -> "InventoryPage":
        self._add_to_cart_button(item_name).click()
        return self

    def remove_item_from_cart(self, item_name: str) -> "InventoryPage":
        self._remove_button(item_name).click()
        return self

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def open_cart(self):
        from pages.cart_page import CartPage

        self.cart_link.click()
        return CartPage(self.page)

    def sort_by(self, option: str) -> "InventoryPage":
        self.sort_dropdown.select_option(option)
        return self

    def get_product_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def get_product_prices(self) -> list[float]:
        raw = self.item_prices.all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def logout(self):
        self.burger_menu_button.click()
        self.logout_link.click()
        from pages.login_page import LoginPage

        return LoginPage(self.page)

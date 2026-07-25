from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")
        self.checkout_button = page.locator("#checkout")
        self.continue_shopping_button = page.locator("#continue-shopping")

    def get_item_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def remove_item(self, item_name: str) -> "CartPage":
        slug = item_name.lower().replace(" ", "-").replace("'", "")
        self.page.locator(f"#remove-{slug}").click()
        return self

    def checkout(self):
        from pages.checkout_page import CheckoutStepOnePage

        self.checkout_button.click()
        return CheckoutStepOnePage(self.page)

    def continue_shopping(self):
        from pages.inventory_page import InventoryPage

        self.continue_shopping_button.click()
        return InventoryPage(self.page)

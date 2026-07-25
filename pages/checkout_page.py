import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    URL = "/checkout-step-one.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.cancel_button = page.locator("#cancel")
        self.error_message = page.locator('[data-test="error"]')

    @allure.step("Fill checkout information")
    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutStepOnePage":
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        return self

    @allure.step("Continue to order overview")
    def continue_to_overview(self):
        from pages.checkout_page import CheckoutStepTwoPage

        self.continue_button.click()
        return CheckoutStepTwoPage(self.page)

    def get_error_text(self) -> str:
        return self.error_message.inner_text()


class CheckoutStepTwoPage(BasePage):
    URL = "/checkout-step-two.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.item_names = page.locator(".inventory_item_name")
        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.total_label = page.locator(".summary_total_label")
        self.finish_button = page.locator("#finish")
        self.cancel_button = page.locator("#cancel")

    def get_item_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def get_subtotal(self) -> float:
        text = self.subtotal_label.inner_text()
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self.total_label.inner_text()
        return float(text.split("$")[-1])

    @allure.step("Finish the order")
    def finish(self):
        from pages.checkout_page import CheckoutCompletePage

        self.finish_button.click()
        return CheckoutCompletePage(self.page)


class CheckoutCompletePage(BasePage):
    URL = "/checkout-complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.complete_header = page.locator(".complete-header")
        self.back_home_button = page.locator("#back-to-products")

    def get_complete_header_text(self) -> str:
        return self.complete_header.inner_text()

    def is_order_complete(self) -> bool:
        return self.complete_header.is_visible()

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator('[data-test="error"]')

    @allure.step("Log in as '{username}'")
    def login(self, username: str, password: str) -> InventoryPage:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return InventoryPage(self.page)

    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def has_error(self) -> bool:
        return self.error_message.is_visible()

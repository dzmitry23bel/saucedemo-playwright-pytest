from playwright.sync_api import Page


class BasePage:
    URL = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)
        return self

    @property
    def current_url(self) -> str:
        return self.page.url

    def title(self) -> str:
        return self.page.title()

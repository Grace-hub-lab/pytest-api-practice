import allure

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/"

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        # 元素定位集中写在 __init__ 里（Locator 是"懒"的，用到时才去页面上找）
        self.username = self.by_test_id("username")
        self.password = self.by_test_id("password")
        self.login_button = self.by_test_id("login-button")
        self.error = self.by_test_id("error")

    @allure.step("登录：{username}")
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

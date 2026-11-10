"""
UI 第 1 课：登录页 —— POM + 数据驱动 + Playwright 断言 expect。

expect(...) 会自动等待（默认最多 5 秒）直到条件满足，所以不用写 sleep。
这是 Playwright 比 Selenium 稳定的主要原因。
"""
import allure
import pytest
from playwright.sync_api import expect

from common.file_loader import load_yaml
from common.paths import DATA_DIR
from ui.pages.inventory_page import InventoryPage

DATA = load_yaml(DATA_DIR / "ui_login.yaml")


@allure.feature("Web-登录")
class TestLogin:

    @pytest.mark.smoke
    def test_login_success(self, login_page, inventory_page, standard_account):
        login_page.open()
        login_page.login(standard_account["username"], standard_account["password"])

        inventory_page.should_have_url(InventoryPage.PATH)
        expect(inventory_page.title).to_have_text("Products")
        expect(inventory_page.items).to_have_count(6)

    @pytest.mark.parametrize("case", DATA["login_fail"], ids=[c["name"] for c in DATA["login_fail"]])
    def test_login_fail(self, login_page, case):
        login_page.open()
        login_page.login(case["username"], case["password"])

        expect(login_page.error).to_be_visible()
        expect(login_page.error).to_contain_text(case["error"])
        login_page.should_have_url("/")        # 没跳转，仍在登录页

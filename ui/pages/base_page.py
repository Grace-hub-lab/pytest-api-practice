"""
Page Object Model（POM）的父类。

POM 的核心思想：
- 每个页面一个类，类里只放「这个页面的元素定位」和「这个页面能做的操作」
- 用例里只调用 login_page.login("user", "pwd")，看不到任何 CSS 选择器
- 页面改版、元素变了，只改 page 类，用例一行不用动

和接口部分的 api/posts_api.py 是完全相同的思路，只是对象从「接口」换成了「页面」。
"""
import allure
from playwright.sync_api import Page, expect


class BasePage:
    # 子类覆盖：页面相对路径，如 "/inventory.html"
    PATH = "/"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self):
        with allure.step(f"打开页面 {self.PATH}"):
            self.page.goto(self.base_url + self.PATH)
        return self

    def by_test_id(self, test_id: str):
        """
        saucedemo 的元素都带 data-test 属性，这是最稳定的定位方式。
        定位优先级（越靠前越稳）：data-test/id > 文本/role > CSS class > XPath
        """
        return self.page.locator(f'[data-test="{test_id}"]')

    def should_have_url(self, path: str):
        expect(self.page).to_have_url(self.base_url + path)

    def screenshot(self, name="截图"):
        allure.attach(self.page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)

"""
ui 目录专用的 conftest.py：只对 ui/ 下的用例生效。

`page` 这个 fixture 由 pytest-playwright 插件提供：每条用例一个全新的浏览器页面，用完自动关闭。
常用命令行参数（插件自带）：
    pytest ui --headed              显示浏览器窗口（默认无头，看不到界面）
    pytest ui --headed --slowmo 500 每步操作慢 500 毫秒，方便看清楚
    pytest ui --browser firefox     换浏览器（需先 playwright install firefox）
"""
import allure
import pytest

from ui.pages.cart_page import CartPage
from ui.pages.checkout_page import CheckoutPage
from ui.pages.inventory_page import InventoryPage
from ui.pages.login_page import LoginPage


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例失败时自动截图，挂到 Allure 报告里（UI 自动化排查问题最重要的手段）。"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            try:
                allure.attach(page.screenshot(full_page=True), name="失败截图",
                              attachment_type=allure.attachment_type.PNG)
            except Exception:  # 浏览器已关闭等情况，截图失败不影响结果
                pass


@pytest.fixture(scope="session")
def ui_base_url(env_config):
    return env_config["ui_base_url"]


@pytest.fixture(scope="session")
def standard_account(app_config):
    return app_config["ui_accounts"]["standard"]


# ---- 页面对象 fixture：用例里直接写参数名就能拿到 ----
@pytest.fixture
def login_page(page, ui_base_url):
    return LoginPage(page, ui_base_url)


@pytest.fixture
def inventory_page(page, ui_base_url):
    return InventoryPage(page, ui_base_url)


@pytest.fixture
def cart_page(page, ui_base_url):
    return CartPage(page, ui_base_url)


@pytest.fixture
def checkout_page(page, ui_base_url):
    return CheckoutPage(page, ui_base_url)


@pytest.fixture
def logged_in(login_page, inventory_page, standard_account):
    """前置条件：已登录并停在商品列表页。需要登录态的用例直接依赖它。"""
    login_page.open()
    login_page.login(standard_account["username"], standard_account["password"])
    inventory_page.should_have_url(InventoryPage.PATH)
    return inventory_page

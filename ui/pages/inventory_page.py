import allure

from ui.pages.base_page import BasePage


class InventoryPage(BasePage):
    """商品列表页（登录后的首页）"""
    PATH = "/inventory.html"

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.title = self.by_test_id("title")
        self.items = page.locator(".inventory_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.sort_select = self.by_test_id("product-sort-container")
        self.cart_badge = self.by_test_id("shopping-cart-badge")
        self.cart_link = self.by_test_id("shopping-cart-link")

    def _item(self, product_name: str):
        """按商品名找到那一张商品卡片（filter + has_text 是 Playwright 很常用的写法）"""
        return self.items.filter(has_text=product_name)

    @allure.step("加入购物车：{product_name}")
    def add_to_cart(self, product_name: str):
        self._item(product_name).get_by_role("button", name="Add to cart").click()

    @allure.step("移出购物车：{product_name}")
    def remove_from_cart(self, product_name: str):
        self._item(product_name).get_by_role("button", name="Remove").click()

    @allure.step("排序：{option}")
    def sort_by(self, option: str):
        """option: az / za / lohi（价格低到高）/ hilo（价格高到低）"""
        self.sort_select.select_option(option)

    def get_prices(self) -> list[float]:
        return [float(t.replace("$", "")) for t in self.item_prices.all_inner_texts()]

    def get_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    @allure.step("进入购物车")
    def go_to_cart(self):
        self.cart_link.click()

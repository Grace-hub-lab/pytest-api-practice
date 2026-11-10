import allure

from ui.pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/cart.html"

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.cart_item_names = page.locator(".cart_item .inventory_item_name")
        self.checkout_button = self.by_test_id("checkout")

    def get_item_names(self) -> list[str]:
        return self.cart_item_names.all_inner_texts()

    @allure.step("点击 Checkout")
    def checkout(self):
        self.checkout_button.click()

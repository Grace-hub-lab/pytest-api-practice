import allure

from ui.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """结算流程：填写信息 -> 订单概览 -> 完成，三个步骤放在一个类里"""
    PATH = "/checkout-step-one.html"

    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.first_name = self.by_test_id("firstName")
        self.last_name = self.by_test_id("lastName")
        self.postal_code = self.by_test_id("postalCode")
        self.continue_button = self.by_test_id("continue")
        self.finish_button = self.by_test_id("finish")
        self.total_label = self.by_test_id("total-label")
        self.complete_header = self.by_test_id("complete-header")
        self.error = self.by_test_id("error")

    @allure.step("填写收货信息")
    def fill_info(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    @allure.step("点击 Finish 完成下单")
    def finish(self):
        self.finish_button.click()

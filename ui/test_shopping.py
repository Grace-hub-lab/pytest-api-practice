"""
UI 第 2 课：商品列表、购物车、下单全流程。
logged_in 是 ui/conftest.py 里的前置 fixture：用例开始时已经登录好了。
"""
import allure
import pytest
from playwright.sync_api import expect

from ui.pages.cart_page import CartPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@allure.feature("Web-商品")
class TestInventory:

    @pytest.mark.parametrize("option, reverse", [("lohi", False), ("hilo", True)],
                             ids=["价格低到高", "价格高到低"])
    def test_sort_by_price(self, logged_in, option, reverse):
        logged_in.sort_by(option)
        prices = logged_in.get_prices()
        assert prices == sorted(prices, reverse=reverse), f"排序不对: {prices}"

    def test_sort_by_name_za(self, logged_in):
        logged_in.sort_by("za")
        names = logged_in.get_names()
        assert names == sorted(names, reverse=True)

    def test_cart_badge_count(self, logged_in):
        """加 2 件 -> 角标 2；移除 1 件 -> 角标 1。"""
        logged_in.add_to_cart(BACKPACK)
        logged_in.add_to_cart(BIKE_LIGHT)
        expect(logged_in.cart_badge).to_have_text("2")

        logged_in.remove_from_cart(BACKPACK)
        expect(logged_in.cart_badge).to_have_text("1")


@allure.feature("Web-下单")
class TestCheckout:

    @pytest.mark.smoke
    def test_checkout_flow(self, logged_in, cart_page, checkout_page):
        """端到端流程：加购 -> 购物车 -> 填信息 -> 完成订单"""
        logged_in.add_to_cart(BACKPACK)
        logged_in.go_to_cart()

        cart_page.should_have_url(CartPage.PATH)
        assert cart_page.get_item_names() == [BACKPACK]
        cart_page.checkout()

        checkout_page.fill_info("Grace", "Test", "518000")
        expect(checkout_page.total_label).to_contain_text("Total")
        checkout_page.finish()

        expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
        checkout_page.screenshot("下单成功")

    def test_checkout_requires_postal_code(self, logged_in, cart_page, checkout_page):
        logged_in.add_to_cart(BACKPACK)
        logged_in.go_to_cart()
        cart_page.checkout()

        checkout_page.fill_info("Grace", "Test", "")
        expect(checkout_page.error).to_contain_text("Postal Code is required")

"""
Android 第 2 课：操作类用例 —— 遥控器按键、启动 app、uiautomator2 找元素。

⚠️ 这些用例会改变设备当前界面（回到主页、打开设置）。
   在别人正在用的设备上不要跑，或者用 pytest android -m "not operate" 排除。
"""
import allure
import pytest

LAUNCHER = "com.amazon.tv.launcher"       # Fire TV 主页
SETTINGS = "com.amazon.tv.settings.v2"    # Fire TV 设置（不同 Fire OS 版本包名可能不同）


@allure.feature("遥控器导航")
@pytest.mark.operate
class TestNavigation:

    def test_home_key_returns_launcher(self, device):
        if not device.is_package_installed(LAUNCHER):
            pytest.skip(f"设备上没有 {LAUNCHER}（不是 Fire TV 或包名不同）")
        device.press("HOME")
        assert device.wait_for_package(LAUNCHER), f"按 HOME 后前台是 {device.current_package()}"

    def test_open_settings_and_back(self, device):
        if not device.is_package_installed(SETTINGS):
            pytest.skip(f"设备上没有 {SETTINGS}，请用 adb shell pm list packages | findstr settings 查实际包名")
        device.start_app(SETTINGS)
        assert device.wait_for_package(SETTINGS)
        device.press("BACK", times=3)
        device.press("HOME")


@allure.feature("uiautomator2")
@pytest.mark.operate
class TestUiautomator2:
    """
    uiautomator2 能读到界面上的元素（文字、resource-id、是否获得焦点）。
    查元素属性：pip install weditor 后运行 python -m weditor，浏览器里能看到界面结构。
    """

    def test_dump_focused_element(self, device):
        d = device.u2                         # 第一次会在设备上安装 u2 服务
        device.press("HOME")
        focused = d(focused=True)
        assert focused.exists(timeout=5), "主页上应该有获得焦点的元素"
        print("\n当前焦点元素:", focused.info.get("text"), focused.info.get("resourceName"))

    def test_dpad_moves_focus(self, device):
        """按右键后，焦点应该移动到另一个元素上（Fire TV 焦点导航的基本检查）"""
        d = device.u2
        device.press("HOME")
        before = d(focused=True).info.get("bounds")
        device.press("RIGHT")
        after = d(focused=True).info.get("bounds")
        assert before != after, "按 RIGHT 后焦点没有移动"

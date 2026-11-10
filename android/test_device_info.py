"""
Android 第 1 课：只读用例 —— 读设备属性做断言，不改变设备任何状态，随时可以跑。
对应日常工作：刷完 build / OTA 之后，检查版本号、型号对不对。
"""
import allure


@allure.feature("设备信息")
class TestDeviceInfo:

    def test_device_online(self, device):
        assert device.adb.get_state() == "device"

    def test_basic_props(self, device):
        model, build, sdk = device.model, device.build_name, device.sdk
        allure.attach(f"serial={device.serial}\nmodel={model}\nbuild={build}\nsdk={sdk}",
                      name="设备信息")
        print(f"\n型号={model}  版本={build}  SDK={sdk}")
        assert model, "ro.product.model 不应为空"
        assert sdk >= 22, f"SDK 版本太低: {sdk}"

    def test_build_is_user(self, device):
        """日常测试用 user build，不是 userdebug / eng。"""
        build_type = device.getprop("ro.build.type")
        print(f"\nro.build.type = {build_type}")
        assert build_type in ("user", "userdebug", "eng")

    def test_amazon_device(self, device):
        """Fire TV 的厂商属性是 Amazon。"""
        assert device.getprop("ro.product.manufacturer").lower() == "amazon"

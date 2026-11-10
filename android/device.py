"""
Fire TV / Android 设备封装（和 api 层、page 层是同一个思路：把底层细节藏起来）。

两层能力：
1. adb 层（adbutils）：读属性、按键、启动 app、截图 —— 不需要在设备上装任何东西
2. UI 层（uiautomator2）：按文字/resource-id 找元素、读界面结构
   —— 第一次连接时会自动在设备上安装 uiautomator2 的服务 apk

Fire TV 和手机最大的区别：没有触摸屏，靠遥控器「焦点」导航。
所以大部分操作是 press("DPAD_DOWN") / press("DPAD_CENTER")，而不是 click(x, y)。
"""
import time

import adbutils

# Fire TV 遥控器按键 -> Android keycode 名称
KEYS = {
    "HOME": "KEYCODE_HOME",
    "BACK": "KEYCODE_BACK",
    "UP": "KEYCODE_DPAD_UP",
    "DOWN": "KEYCODE_DPAD_DOWN",
    "LEFT": "KEYCODE_DPAD_LEFT",
    "RIGHT": "KEYCODE_DPAD_RIGHT",
    "OK": "KEYCODE_DPAD_CENTER",
    "MENU": "KEYCODE_MENU",
    "PLAY_PAUSE": "KEYCODE_MEDIA_PLAY_PAUSE",
}


class FireTVDevice:
    def __init__(self, serial: str | None = None):
        devices = adbutils.adb.device_list()
        if not devices:
            raise RuntimeError("没有检测到 adb 设备，请先 adb connect <IP> 或插上 USB")
        serials = [d.serial for d in devices]
        if serial and serial not in serials:
            raise RuntimeError(f"找不到设备 {serial}，当前已连接: {serials}")
        self.adb = adbutils.adb.device(serial=serial) if serial else devices[0]
        self.serial = self.adb.serial
        self._u2 = None

    # ---------- 只读信息 ----------
    def getprop(self, name: str) -> str:
        return self.adb.shell(f"getprop {name}").strip()

    @property
    def model(self) -> str:
        return self.getprop("ro.product.model")

    @property
    def build_name(self) -> str:
        """Fire OS 的版本名，例如 Fire OS 8.1.x"""
        return self.getprop("ro.build.version.name") or self.getprop("ro.build.display.id")

    @property
    def sdk(self) -> int:
        return int(self.getprop("ro.build.version.sdk"))

    def current_package(self) -> str:
        return self.adb.app_current().package

    def is_package_installed(self, package: str) -> bool:
        return package in self.adb.list_packages()

    # ---------- 操作（会改变设备当前界面）----------
    def press(self, key: str, times: int = 1, interval: float = 0.5):
        """遥控器按键：press("DOWN", times=3)"""
        code = KEYS.get(key.upper(), key)
        for _ in range(times):
            self.adb.keyevent(code)
            time.sleep(interval)

    def start_app(self, package: str):
        self.adb.app_start(package)

    def wait_for_package(self, package: str, timeout: float = 10) -> bool:
        """等待某个 app 来到前台（UI 自动化里"等待"永远比 sleep 固定时间可靠）"""
        end = time.time() + timeout
        while time.time() < end:
            if self.current_package() == package:
                return True
            time.sleep(0.5)
        return False

    def screenshot(self, path: str):
        self.adb.screenshot().save(path)

    # ---------- uiautomator2（按需连接）----------
    @property
    def u2(self):
        """第一次访问时才连接 uiautomator2（会在设备上安装服务 apk）"""
        if self._u2 is None:
            import uiautomator2
            self._u2 = uiautomator2.connect(self.serial)
        return self._u2

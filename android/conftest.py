"""
android 目录专用 conftest。

运行方式（不会被默认的 pytest 跑到，必须指定目录）：
    pytest android                         # 自动用第一台 adb 设备
    pytest android --serial 192.168.1.10:5555
    pytest android -m "not operate"        # 只跑只读用例，不按键、不动设备界面

没有连设备时，这里的用例会全部 skip（跳过），不会报错。
"""
import allure
import pytest

from android.device import FireTVDevice


def pytest_addoption(parser):
    parser.addoption("--serial", action="store", default=None, help="adb 设备序列号或 IP:端口")


def pytest_configure(config):
    config.addinivalue_line("markers", "operate: 会操作设备（按键/启动 app），只想读信息时用 -m 'not operate' 排除")


@pytest.fixture(scope="session")
def device(request):
    try:
        return FireTVDevice(request.config.getoption("--serial"))
    except Exception as e:  # 没装 adb、没连设备都走这里
        pytest.skip(f"跳过 Android 用例：{e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """失败时截取设备屏幕挂到 Allure。"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "device" in item.funcargs:
        try:
            img = item.funcargs["device"].adb.screenshot()
            import io
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            allure.attach(buf.getvalue(), name="设备截图", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

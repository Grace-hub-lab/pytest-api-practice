"""
第 5 课：面向对象（class）—— 自动化框架最核心的语法
本项目的 HttpClient、PostsApi、LoginPage 全都是 class。
运行：python playground/lesson05_oop.py
"""


# ---------- 1. 定义类、创建对象 ----------
class Device:
    # __init__：创建对象时自动执行，用来初始化属性
    def __init__(self, name, dsn, build="unknown"):
        self.name = name        # self.xxx 是这个对象自己的属性
        self.dsn = dsn
        self.build = build
        self.online = False

    # 方法：类里的函数，第一个参数永远是 self
    def connect(self):
        self.online = True
        print(f"{self.name} 已连接")

    def upgrade(self, new_build):
        if not self.online:
            print("设备离线，无法升级")
            return False
        print(f"{self.name}: {self.build} -> {new_build}")
        self.build = new_build
        return True

    # __str__：print(对象) 时显示的内容
    def __str__(self):
        return f"Device({self.name}, {self.dsn}, {self.build})"


tv = Device("Curiosity", "GCP53E0060730008", "Ship1019#4")   # 创建对象（实例）
tv.upgrade("Ship1019#5")       # 离线时升级失败
tv.connect()
tv.upgrade("Ship1019#5")
print(tv)

tv2 = Device("Hylight", "G0000000000001")   # 每个对象的属性互相独立
print(tv2, "在线?", tv2.online)


# ---------- 2. 继承：子类自动拥有父类的属性和方法 ----------
class FireTV(Device):
    def __init__(self, name, dsn, build="unknown", region="US"):
        super().__init__(name, dsn, build)     # 调用父类的 __init__
        self.region = region

    # 重写父类方法
    def connect(self):
        super().connect()
        print(f"  区域: {self.region}")

    # 子类新增的方法
    def press_key(self, key):
        print(f"  按键 {key}")


ftv = FireTV("Anthem", "G1111111111111", region="EU")
ftv.connect()
ftv.press_key("HOME")
print("是 Device 吗?", isinstance(ftv, Device))


# ---------- 3. 和本项目的对应关系 ----------
# UI 自动化的 Page Object 就是这样用继承的：
class BasePage:
    """所有页面的公共操作写在父类"""

    def __init__(self, page):
        self.page = page

    def open(self, url):
        print(f"[{self.__class__.__name__}] 打开 {url}")


class LoginPage(BasePage):
    """每个页面一个子类，只写自己页面的元素和操作"""
    USERNAME = "#user-name"       # 类属性：所有对象共享，适合放元素定位

    def login(self, user, pwd):
        print(f"在 {self.USERNAME} 输入 {user}，密码 {'*' * len(pwd)}，点登录")


lp = LoginPage(page="假装是浏览器页面")
lp.open("https://www.saucedemo.com")
lp.login("standard_user", "secret_sauce")


# ---------- 4. 类方法 / 静态方法（读源码会遇到）----------
class Utils:
    @staticmethod
    def is_success(code):          # 不需要 self，就是放在类里的普通函数
        return 200 <= code < 300


print("201 成功?", Utils.is_success(201))

# ============ 课后练习 ============
# 1. 写一个 TestResult 类：属性 case_id、status；方法 is_passed() 返回布尔
# 2. 写一个 TestRun 类：内部用列表保存多个 TestResult；
#    方法 add(result)、pass_rate()、summary()（返回 {"passed": n, "failed": m}）
# 3. 打开 common/http_client.py，说出：类名、__init__ 里有哪些属性、有哪些方法

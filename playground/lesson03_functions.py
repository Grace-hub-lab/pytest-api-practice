"""
第 3 课：函数
运行：python playground/lesson03_functions.py
"""


# ---------- 1. 定义和调用 ----------
def say_hello(name):
    print(f"Hello, {name}")


say_hello("Grace")


# ---------- 2. 返回值 ----------
def pass_rate(passed, total):
    if total == 0:
        return 0.0
    return passed / total


rate = pass_rate(8, 10)
print(f"通过率: {rate:.0%}")


# ---------- 3. 默认参数 & 关键字参数 ----------
def send_request(url, method="GET", timeout=15):
    print(f"{method} {url} (timeout={timeout})")


send_request("/posts")                          # 用默认值
send_request("/posts", method="POST")           # 按名字传，顺序无所谓
send_request(timeout=30, url="/users")


# ---------- 4. 返回多个值 ----------
def split_build(build):
    """'Ship1019#5' -> ('Ship1019', 5)"""
    line, number = build.split("#")
    return line, int(number)


line, num = split_build("Ship1019#5")
print("线:", line, "号:", num)


# ---------- 5. *args 和 **kwargs（读框架源码时经常见到）----------
def log(*args, **kwargs):
    print("位置参数 args:", args)        # 元组
    print("关键字参数 kwargs:", kwargs)  # 字典


log(1, 2, 3, level="INFO", tag="api")

# 本项目 common/http_client.py 里的 request(self, method, path, **kwargs)
# 就是用 **kwargs 把 params / json / headers 原样透传给 requests。


# ---------- 6. 类型提示（可选，让代码更清楚，不影响运行）----------
def add(a: int, b: int) -> int:
    return a + b


print(add(1, 2))


# ---------- 7. 函数也能当参数传（装饰器的基础）----------
def run_twice(func):
    func()
    func()


run_twice(lambda: print("被调用了"))


# ---------- 8. 装饰器：@xxx 写在函数上方（pytest 的 @pytest.fixture 就是装饰器）----------
def timer(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时 {(time.time() - start) * 1000:.1f} ms")
        return result

    return wrapper


@timer
def slow_task():
    sum(range(1_000_000))


slow_task()

# ============ 课后练习 ============
# 1. 写函数 is_success(status_code)，2xx 返回 True，否则 False
# 2. 写函数 parse_version_code(filename)，从 bin 文件名里返回 13 位 version code（int）
# 3. 写一个装饰器 retry，被装饰的函数抛异常时最多重试 3 次（学完第 4 课异常再做）

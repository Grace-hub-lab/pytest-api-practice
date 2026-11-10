"""
第 4 课：异常处理、文件读写、JSON / YAML、模块导入
运行：python playground/lesson04_errors_files.py
"""
import json
from pathlib import Path

import yaml  # 第三方库，已在 requirements.txt 里

# ---------- 1. try / except ----------
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("捕获到异常:", e)

data = {"id": 1}
try:
    print(data["title"])
except KeyError as e:
    print("缺少字段:", e)
finally:
    print("finally 无论成功失败都会执行（常用于清理资源）")

# 主动抛异常：assert 失败其实就是抛出 AssertionError
try:
    assert 1 == 2, "期望相等"
except AssertionError as e:
    print("断言失败:", e)


# 自定义异常
class DeviceOfflineError(Exception):
    pass


def check_device(online):
    if not online:
        raise DeviceOfflineError("设备离线")
    return "OK"


try:
    check_device(False)
except DeviceOfflineError as e:
    print("自定义异常:", e)

# ---------- 2. 文件读写（Path 是现代写法）----------
tmp_dir = Path(__file__).parent / "_tmp"
tmp_dir.mkdir(exist_ok=True)

txt = tmp_dir / "log.txt"
txt.write_text("第一行\n第二行\n", encoding="utf-8")       # encoding 一定写 utf-8，避免中文乱码
with open(txt, "a", encoding="utf-8") as f:               # "a" 追加；"w" 覆盖；"r" 读
    f.write("追加的一行\n")

with open(txt, encoding="utf-8") as f:                    # with 会自动关闭文件
    for line in f:
        print("读到:", line.strip())

# ---------- 3. JSON：接口数据的格式 ----------
post = {"id": 1, "title": "中文标题", "tags": ["api", "smoke"]}

json_str = json.dumps(post, ensure_ascii=False, indent=2)   # dict -> 字符串
print("JSON 字符串:\n", json_str)
back = json.loads(json_str)                                 # 字符串 -> dict
print("转回字典:", back["title"])

(tmp_dir / "post.json").write_text(json_str, encoding="utf-8")

# ---------- 4. YAML：本项目测试数据的格式 ----------
yaml_text = """
login:
  - name: 正确账号
    user: standard_user
    ok: true
  - name: 锁定账号
    user: locked_out_user
    ok: false
"""
cases = yaml.safe_load(yaml_text)
for c in cases["login"]:
    print("YAML 用例:", c["name"], c["user"], c["ok"])

# ---------- 5. 模块导入 ----------
# import json                     导入整个模块，用 json.dumps
# from pathlib import Path        只导入需要的名字
# from common.paths import ROOT   导入本项目自己的模块（要在项目根目录运行）
print("本文件所在目录:", Path(__file__).parent)

# ============ 课后练习 ============
# 1. 读取项目里的 data/posts.yaml，打印 get_post 下每条用例的 name
#    提示：Path(__file__).parent.parent / "data" / "posts.yaml"
# 2. 写函数 safe_int(s)：能转成 int 就返回，转不了返回 None（用 try/except ValueError）
# 3. 把 [{"case": 1, "result": "passed"}, ...] 写入 results.json，再读回来统计通过数

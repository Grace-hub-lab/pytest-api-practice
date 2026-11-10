"""
第 1 课：变量与数据类型
运行：python playground/lesson01_types.py
建议：边看输出边改代码，改完再运行，看结果怎么变。
"""

# ---------- 1. 基本类型 ----------
name = "Fire TV"        # str 字符串
version = 1019          # int 整数
pass_rate = 0.95        # float 小数
is_ship = True          # bool 布尔：True / False
nothing = None          # None 表示"没有值"

print("type 看类型:", type(name), type(version), type(pass_rate), type(is_ship))

# ---------- 2. 字符串常用操作 ----------
build = "Ship1019#5"
print(f"f-string 拼接: 设备={name}, 版本={version}")   # 最常用的拼接方式
print("长度:", len(build))
print("切片 [0:4]:", build[0:4])                        # 取前 4 个字符 -> Ship
print("包含判断:", "1019" in build)
print("分割:", build.split("#"))                         # ['Ship1019', '5']
print("替换:", build.replace("Ship", "ML"))
print("大小写:", name.upper(), name.lower())
print("去掉首尾空格:", "  hello  ".strip())

# ---------- 3. 列表 list：有顺序，可修改 ----------
devices = ["Curiosity", "Hylight", "Anthem"]
devices.append("Malmo")             # 末尾添加
print("列表:", devices)
print("第一个:", devices[0], "最后一个:", devices[-1])
print("个数:", len(devices))
devices.remove("Hylight")           # 按值删除
print("删除后:", devices)

# ---------- 4. 字典 dict：键值对（接口返回的 JSON 就是字典！）----------
post = {"id": 1, "title": "hello", "userId": 1}
print("取值:", post["title"])
print("安全取值(键不存在返回默认):", post.get("body", "无内容"))
post["body"] = "new body"           # 新增 / 修改
print("所有键:", list(post.keys()))
print("键是否存在:", "id" in post)

# 嵌套：列表里放字典，接口返回列表数据时就是这个结构
users = [
    {"name": "Grace", "age": 18},
    {"name": "Tom", "age": 20},
]
print("第二个人的名字:", users[1]["name"])

# ---------- 5. 元组 tuple 和 集合 set ----------
point = (10, 20)                    # 元组：不能修改
tags = {"smoke", "api", "smoke"}    # 集合：自动去重
print("元组:", point, "集合:", tags)

# ---------- 6. 类型转换 ----------
print(int("123") + 1, str(456) + "!", float("3.5"), list("abc"))

# ============ 课后练习（写在下面，运行验证）============
# 1. 定义一个字典 device，包含 name、dsn、build 三个键，用 f-string 打印一句话
# 2. 从字符串 "update-kindle-curiosity_user_5_0030735860612.bin" 中，
#    用 split 取出最后的 13 位数字（提示：先按 "_" 分，再去掉 ".bin"）
# 3. 给 users 列表再加一个人，然后打印所有人的名字

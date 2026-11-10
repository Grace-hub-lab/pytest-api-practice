"""
第 2 课：条件判断与循环
运行：python playground/lesson02_control_flow.py
"""

# ---------- 1. if / elif / else ----------
status_code = 404

if status_code == 200:
    print("成功")
elif status_code == 404:
    print("资源不存在")
elif status_code >= 500:
    print("服务器错误")
else:
    print("其他状态:", status_code)

# 组合条件：and / or / not
age, has_ticket = 20, True
if age >= 18 and has_ticket:
    print("可以入场")

# ---------- 2. for 循环 ----------
results = ["passed", "failed", "passed", "skipped", "passed"]

for r in results:
    print("结果:", r)

# enumerate：同时拿到序号和值
for i, r in enumerate(results, start=1):
    print(f"第 {i} 条: {r}")

# range：生成数字序列
for n in range(3):          # 0, 1, 2
    print("重试第", n + 1, "次")

# 遍历字典
counts = {"passed": 3, "failed": 1}
for status, num in counts.items():
    print(status, "->", num)

# ---------- 3. break / continue ----------
for r in results:
    if r == "skipped":
        continue            # 跳过本次，继续下一个
    if r == "failed":
        print("发现失败，停止检查")
        break               # 直接结束整个循环

# ---------- 4. while 循环（常用于"等待某个条件"）----------
retry = 0
while retry < 3:
    retry += 1
    print("等待设备上线... 第", retry, "次")

# ---------- 5. 列表推导式（自动化代码里非常常见）----------
nums = [1, 2, 3, 4, 5]
squares = [n * n for n in nums]                 # 每个元素做运算
evens = [n for n in nums if n % 2 == 0]         # 过滤
print("平方:", squares, "偶数:", evens)

passed = [r for r in results if r == "passed"]
print("通过数:", len(passed))
print("全部通过?", all(r == "passed" for r in results))
print("有失败?", any(r == "failed" for r in results))

# ============ 课后练习 ============
# 1. 统计 results 中每种状态出现了几次，存进一个字典并打印（不能用 Counter）
# 2. 计算通过率（passed 数 / 总数），格式化成百分比打印，如 "通过率: 60.0%"
#    提示：f"{rate:.1%}"
# 3. 用 while 写一个"最多重试 5 次，第 3 次成功就停止"的逻辑

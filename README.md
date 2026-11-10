# 自动化测试练习项目

[![tests](https://github.com/Grace-hub-lab/pytest-api-practice/actions/workflows/tests.yml/badge.svg)](https://github.com/Grace-hub-lab/pytest-api-practice/actions/workflows/tests.yml)

一个仓库覆盖测试开发的完整学习路线：

| 模块 | 技术 | 练习对象 | 目录 |
|---|---|---|---|
| Python 基础 | 5 课可运行示例 + 课后题 | — | `playground/` |
| 接口自动化 | pytest + requests + YAML 数据驱动 + JSON Schema | [JSONPlaceholder](https://jsonplaceholder.typicode.com) | `testcases/` |
| Web UI 自动化 | Playwright + Page Object | [saucedemo](https://www.saucedemo.com) | `ui/` |
| Android / Fire TV | adbutils + uiautomator2 | 真机（adb 连接） | `android/` |
| 报告 | pytest-html、Allure（失败自动截图） | — | `reports/` |
| 持续集成 | GitHub Actions：每次 push 自动跑 | — | `.github/workflows/` |

> 📘 **第一次使用 / 在家里电脑从零开始**：看 [docs/家里电脑学习指南.md](docs/家里电脑学习指南.md)，包含安装步骤、在哪执行命令、按周学习计划和视频资料。

## 目录结构

```
├── playground/                 # 阶段1：Python 基础，每课一个文件，直接运行
│   ├── lesson01_types.py       #   变量、字符串、列表、字典
│   ├── lesson02_control_flow.py#   if / for / while / 列表推导式
│   ├── lesson03_functions.py   #   函数、参数、装饰器
│   ├── lesson04_errors_files.py#   异常、文件、JSON、YAML
│   └── lesson05_oop.py         #   类、继承（框架核心）
│
├── config/config.yaml          # 多环境配置（接口地址、UI 地址、账号）
├── common/                     # 通用工具层
│   ├── http_client.py          #   requests 封装：base_url、日志、Allure 附件
│   ├── assertions.py           #   断言封装：状态码、字段、Schema
│   ├── file_loader.py          #   读 YAML / JSON
│   └── paths.py                #   项目路径
├── data/                       # 测试数据（数据驱动）
│   ├── posts.yaml / users.yaml #   接口用例数据
│   ├── ui_login.yaml           #   UI 登录用例数据
│   └── schemas/                #   JSON Schema（响应结构校验）
│
├── api/                        # 阶段3：接口层（API Object：一个业务模块一个类）
│   ├── posts_api.py
│   └── users_api.py
├── testcases/                  # 阶段2～3：接口用例
│   ├── test_01_basics.py       #   原生 pytest + requests
│   ├── test_02_posts.py        #   fixture + 参数化 + 封装 + Schema
│   ├── test_03_flow.py         #   接口关联 + yield 前后置
│   └── test_04_users.py        #   嵌套 Schema + 查询参数
│
├── ui/                         # 阶段4：Web UI 自动化
│   ├── pages/                  #   Page Object：一个页面一个类
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── conftest.py             #   页面 fixture、登录前置、失败截图
│   ├── test_login.py           #   登录（数据驱动）
│   └── test_shopping.py        #   排序、购物车、下单全流程
│
├── android/                    # 阶段4：Fire TV / Android 设备自动化
│   ├── device.py               #   设备封装：属性、遥控器按键、uiautomator2
│   ├── conftest.py             #   --serial 参数、无设备自动跳过、失败截屏
│   ├── test_device_info.py     #   只读用例（版本号、型号）
│   └── test_navigation.py      #   操作用例（按键、焦点导航）⚠️会改变设备界面
│
├── .github/workflows/tests.yml # 阶段5：CI，push 后自动跑接口 + UI
├── conftest.py                 # 全局 fixture、--env 参数、按目录自动打标记
├── pytest.ini                  # pytest 配置
├── run.py                      # 一键运行 + 生成报告
└── requirements.txt            # 依赖（固定版本）
```

## 快速开始

```powershell
git clone https://github.com/Grace-hub-lab/pytest-api-practice.git
cd pytest-api-practice
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium     # Web UI 用的浏览器，只需一次
python run.py
```

看到 **`30 passed`**（19 条接口 + 11 条 Web UI）就成功了。详细步骤和报错处理见 [学习指南](docs/家里电脑学习指南.md)。

## 常用命令

| 命令 | 作用 |
|---|---|
| `python run.py` | 跑接口 + UI，生成 `reports/report.html` |
| `pytest` | 跑接口 + UI（不生成报告） |
| `pytest -m api` / `pytest -m ui` | 只跑接口 / 只跑 Web UI |
| `pytest -m smoke` | 只跑冒烟用例 |
| `pytest testcases/test_02_posts.py` | 只跑一个文件 |
| `pytest -k create` | 只跑名字含 create 的用例 |
| `pytest -x` / `pytest --lf` | 遇到失败就停 / 只重跑上次失败的 |
| `pytest --env=dev` | 切换环境 |
| `pytest ui --headed --slowmo 500` | **显示浏览器窗口**，每步慢 0.5 秒（学 UI 时最常用） |
| `pytest android -m "not operate"` | 设备只读用例（不动设备界面） |
| `pytest android --serial <序列号>` | 指定设备跑全部 Android 用例 |
| `python playground/lesson01_types.py` | 运行 Python 练习课 |

## 查看报告

- **HTML 报告**：`python run.py` 后双击 `reports/report.html`
- **Allure 报告**（更漂亮，有步骤、请求响应、失败截图）：需要先安装 [Java 17+](https://adoptium.net/) 和 Allure（[Scoop](https://scoop.sh) 安装：`scoop install allure`，或从 [Releases](https://github.com/allure-framework/allure2/releases) 下载 zip、把 `bin` 加入 PATH），然后 `allure serve allure-results`
- **CI 报告**：GitHub 仓库 → **Actions** → 点某次运行 → 页面底部 **Artifacts** → 下载 `test-reports`

## 两台电脑之间同步

```powershell
git pull                      # 开始前：拉取另一台电脑的改动
# ……写代码……
git add .
git commit -m "描述你改了什么"
git push                      # 结束后：推上去，CI 会自动跑一遍
```

## 练习题

做之前先 `git pull`，做完 `git push`，在 Actions 页面看 CI 是否通过。

**接口**
1. 在 `data/posts.yaml` 的 `get_post` 里加一条 `post_id: 50`，不改代码，看用例数是否 +1
2. 故意把一条期望值改错，看失败信息长什么样，再改回来
3. 新增 `api/comments_api.py`，封装 `/comments?postId=1`，写 `testcases/test_05_comments.py`
4. 给 comment 写 JSON Schema，要求 `email` 字段符合邮箱格式
5. 写流程用例：查相册 `/albums?userId=1` → 取第一个相册 → 查照片 `/photos?albumId=x` → 断言每张照片的 `albumId` 正确
6. 在 `conftest.py` 加一个 `autouse=True` 的 fixture，打印每条用例的耗时

**Web UI**
7. 用 `pytest ui --headed --slowmo 500` 看浏览器怎么动，对照 `ui/pages/` 读代码
8. 在 `data/ui_login.yaml` 加一条 `problem_user` 登录成功的数据（需要改用例让它支持"期望成功"）
9. 给 `InventoryPage` 加 `open_product(name)`，新建 `ProductPage`，测试商品详情页的名称和价格与列表页一致
10. 测试 "Reset App State" 菜单：加购后重置，购物车角标消失

**Android / Fire TV**（在自己的设备上做）
11. 给 `test_device_info.py` 加一条：检查 `ro.build.version.sdk` 是否等于你期望的值（从 YAML 读）
12. 写一个用例：按 HOME → 按 DOWN 3 次 → 截图保存到 `reports/`
13. 用 `python -m weditor`（先 `pip install weditor`）查看设置页的元素，写一个 uiautomator2 用例打开某个设置项

**工程化**
14. 用 `pytest -n 4` 并发跑接口用例（先 `pip install pytest-xdist`），对比耗时
15. 修改 CI：每天早上 8 点自动跑一次（提示：`on.schedule.cron`，注意 UTC 时区）

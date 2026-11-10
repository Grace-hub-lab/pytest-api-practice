# pytest 接口自动化练习框架

pytest + requests + YAML 数据驱动 + JSON Schema + Allure / HTML 报告。
练习接口：[JSONPlaceholder](https://jsonplaceholder.typicode.com)（免费，无需注册）。

## 目录结构

```
auto/
├── config/config.yaml      # 多环境配置（base_url、超时）
├── common/                 # 通用工具层
│   ├── http_client.py      #   requests 封装：base_url、日志、Allure 附件
│   ├── assertions.py       #   断言封装：状态码、字段、Schema
│   ├── file_loader.py      #   读 YAML / JSON
│   └── paths.py            #   项目路径
├── api/posts_api.py        # 接口层：一个业务模块一个类（API Object）
├── data/
│   ├── posts.yaml          # 测试数据（数据驱动）
│   └── schemas/post.json   # 响应结构校验
├── testcases/              # 用例层
│   ├── test_01_basics.py   #   第1课：原生 pytest + requests
│   ├── test_02_posts.py    #   第2课：fixture + 参数化 + 封装
│   └── test_03_flow.py     #   第3课：接口关联 + 前后置
├── conftest.py             # 全局 fixture、--env 命令行参数
├── pytest.ini              # pytest 配置
├── run.py                  # 一键运行 + 生成报告
└── requirements.txt        # 依赖（固定版本）
```

建议阅读顺序：`test_01` → `conftest.py` → `common/http_client.py` → `api/posts_api.py` → `test_02` → `test_03`。

## 新电脑上第一次使用（家里电脑也一样）

1. 安装 [Python 3.11+](https://www.python.org/downloads/)（安装时勾选 **Add python.exe to PATH**）和 [Git](https://git-scm.com/download/win)
2. 拉代码并安装依赖（PowerShell）：

```powershell
git clone https://github.com/Grace-hub-lab/pytest-api-practice.git
cd pytest-api-practice
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # 激活虚拟环境，提示符前出现 (.venv)
pip install -r requirements.txt
```

> 如果 `Activate.ps1` 报"禁止运行脚本"，先执行一次：
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

3. 跑一下：`python run.py`，看到 `12 passed` 就成功了。

## 两台电脑之间同步

```powershell
git pull                      # 开始写之前：拉取另一台电脑的改动
# ……写代码……
git add .
git commit -m "描述你改了什么"
git push                      # 写完：推上去
```

养成"先 pull 再写，写完就 push"的习惯，就不会冲突。

## 常用命令

| 命令 | 作用 |
|---|---|
| `pytest` | 跑全部用例 |
| `pytest testcases/test_02_posts.py` | 只跑一个文件 |
| `pytest -k create` | 只跑名字含 create 的用例 |
| `pytest -m smoke` | 只跑标了 smoke 的用例 |
| `pytest --env=dev` | 切换环境 |
| `pytest -x` | 遇到第一个失败就停 |
| `pytest --lf` | 只重跑上次失败的 |
| `python run.py` | 跑全部 + 生成 `reports/report.html` |

## 查看 Allure 报告（可选）

Allure 需要 Java 和 Allure 命令行工具：

1. 安装 [Java 17+](https://adoptium.net/)
2. 安装 Allure（用 [Scoop](https://scoop.sh)：`scoop install allure`，或从 [GitHub Releases](https://github.com/allure-framework/allure2/releases) 下载 zip 解压，把 `bin` 加入 PATH）
3. `python run.py` 之后执行 `allure serve allure-results`，浏览器会自动打开报告

没装 Allure 也没关系，`reports/report.html` 直接双击就能看。

## 练习题（由易到难）

1. 在 `data/posts.yaml` 的 `get_post` 里加一条 `post_id: 50` 的数据，不改代码，看用例数是否 +1
2. 故意把一条期望值改错，跑一下，看失败信息长什么样，再改回来
3. 新增 `api/users_api.py`，封装 `/users` 和 `/users/{id}`，并写 `testcases/test_04_users.py`
4. 给 user 写一个 JSON Schema（`data/schemas/user.json`），校验 `address`、`company` 这类嵌套对象
5. 写一个流程用例：查用户 → 查他的 todos（`/users/{id}/todos`）→ 断言 completed 字段都是布尔值
6. 给 `conftest.py` 加一个 fixture，统计并打印每条用例的耗时
7. 用 `pytest -n 4` 并发跑（需要先 `pip install pytest-xdist`）
8. 进阶：写一个 GitHub Actions 工作流，每次 push 自动跑用例

"""
根目录 conftest.py：pytest 会自动加载，这里定义的 fixture 所有用例都能直接用（不用 import）。

fixture 作用域（scope）：
- function（默认）：每条用例都执行一次
- module：每个 .py 文件执行一次
- session：整个测试运行只执行一次 —— 适合配置、HTTP 客户端、登录
"""
import pytest

from api.posts_api import PostsApi
from common.file_loader import load_yaml
from common.http_client import HttpClient
from common.paths import CONFIG_DIR


def pytest_addoption(parser):
    """自定义命令行参数：pytest --env=dev"""
    parser.addoption("--env", action="store", default=None, help="运行环境: test / dev")


@pytest.fixture(scope="session")
def env_config(request):
    config = load_yaml(CONFIG_DIR / "config.yaml")
    env = request.config.getoption("--env") or config["default_env"]
    if env not in config["envs"]:
        raise pytest.UsageError(f"未知环境 '{env}'，可选: {list(config['envs'])}")
    return config["envs"][env]


@pytest.fixture(scope="session")
def http_client(env_config):
    client = HttpClient(env_config["base_url"], timeout=env_config["timeout"])
    yield client            # yield 之前是 setup，之后是 teardown
    client.session.close()  # 全部用例跑完后关闭连接


@pytest.fixture(scope="session")
def posts_api(http_client):
    return PostsApi(http_client)

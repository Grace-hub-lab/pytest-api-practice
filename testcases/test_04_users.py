"""
第 4 课：嵌套结构的 Schema 校验 + 查询参数 + 自己在用例文件里定义 fixture。
users_api 来自根目录 conftest.py。
"""
import allure
import pytest

from common.assertions import assert_fields, assert_schema, assert_status
from common.file_loader import load_yaml
from common.paths import DATA_DIR

DATA = load_yaml(DATA_DIR / "users.yaml")


@allure.feature("用户管理")
class TestUsers:

    @pytest.mark.smoke
    def test_list_users(self, users_api):
        resp = users_api.list_users()
        assert_status(resp, 200)
        users = resp.json()
        assert len(users) == 10
        # 每个用户都要通过结构校验（包括 address.geo 这种嵌套对象）
        for u in users:
            assert_schema(u, "user.json")

    @pytest.mark.parametrize("case", DATA["get_user"], ids=[c["name"] for c in DATA["get_user"]])
    def test_get_user(self, users_api, case):
        resp = users_api.get_user(case["user_id"])
        assert_status(resp, 200)
        assert_fields(resp.json(), case["expected"])

    def test_usernames_unique(self, users_api):
        names = [u["username"] for u in users_api.list_users().json()]
        assert len(names) == len(set(names)), "username 有重复"


@allure.feature("用户管理")
class TestTodos:

    @pytest.mark.parametrize("completed", [True, False])
    def test_filter_todos_by_completed(self, users_api, completed):
        """查询参数过滤：返回的每一条 completed 字段都应等于过滤值。"""
        resp = users_api.list_todos(1, completed=completed)
        assert_status(resp, 200)
        todos = resp.json()
        assert todos, "过滤后不应为空"
        assert all(t["completed"] is completed for t in todos)

    def test_todo_count_adds_up(self, users_api):
        """完成数 + 未完成数 = 总数。"""
        total = len(users_api.list_todos(1).json())
        done = len(users_api.list_todos(1, completed=True).json())
        undone = len(users_api.list_todos(1, completed=False).json())
        assert done + undone == total

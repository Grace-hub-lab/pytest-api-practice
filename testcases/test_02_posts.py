"""
第 2 课：用框架写用例 —— fixture + 数据驱动(YAML) + 封装断言 + Allure。

posts_api 这个参数不是自己创建的，是 conftest.py 里的 fixture，pytest 按名字自动注入。
"""
import allure
import pytest

from common.assertions import assert_fields, assert_schema, assert_status
from common.file_loader import load_yaml
from common.paths import DATA_DIR

DATA = load_yaml(DATA_DIR / "posts.yaml")


@allure.feature("帖子管理")
class TestPosts:

    @allure.story("查询帖子")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "case", DATA["get_post"], ids=[c["name"] for c in DATA["get_post"]]
    )
    def test_get_post(self, posts_api, case):
        resp = posts_api.get_post(case["post_id"])

        assert_status(resp, case["expected_status"])
        if resp.status_code == 200:
            assert_fields(resp.json(), case["expected"])
            assert_schema(resp.json(), "post.json")

    @allure.story("创建帖子")
    @pytest.mark.parametrize(
        "case", DATA["create_post"], ids=[c["name"] for c in DATA["create_post"]]
    )
    def test_create_post(self, posts_api, case):
        resp = posts_api.create_post(case["title"], case["body"], case["user_id"])

        assert_status(resp, 201)
        data = resp.json()
        assert_fields(data, {"title": case["title"], "body": case["body"], "userId": case["user_id"]})
        assert "id" in data, "创建成功应返回新 id"

    @allure.story("修改帖子")
    @pytest.mark.regression
    def test_update_title(self, posts_api):
        resp = posts_api.update_title(1, "new title")
        assert_status(resp, 200)
        assert_fields(resp.json(), {"id": 1, "title": "new title"})

    @allure.story("删除帖子")
    @pytest.mark.regression
    def test_delete_post(self, posts_api):
        resp = posts_api.delete_post(1)
        assert_status(resp, 200)

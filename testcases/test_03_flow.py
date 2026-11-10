"""
第 3 课：接口关联（业务流程用例）—— 上一个接口的返回值，作为下一个接口的入参。

真实项目最常见的例子：登录拿 token -> 带 token 调其他接口。
这里用「查用户的帖子 -> 取第一篇的 id -> 查这篇的评论」来演示同样的思路。
"""
import allure
import pytest

from common.assertions import assert_status


@allure.feature("业务流程")
@pytest.mark.smoke
def test_user_post_comments_flow(posts_api):
    with allure.step("第 1 步：查询用户 2 的帖子"):
        resp = posts_api.list_posts_by_user(2)
        assert_status(resp, 200)
        posts = resp.json()
        assert posts, "用户 2 应该有帖子"

    first_post_id = posts[0]["id"]  # 提取数据，传给下一步

    with allure.step(f"第 2 步：查询帖子 {first_post_id} 的评论"):
        resp = posts_api.list_comments(first_post_id)
        assert_status(resp, 200)
        comments = resp.json()

    with allure.step("第 3 步：校验评论都属于这篇帖子"):
        assert all(c["postId"] == first_post_id for c in comments)
        assert all("@" in c["email"] for c in comments), "email 格式不对"


@pytest.fixture
def created_post(posts_api):
    """
    function 级 fixture 的典型用法：用例前准备数据，用例后清理数据。
    yield 前 = 前置（造数据），yield 后 = 后置（删数据），用例失败也会执行后置。
    """
    resp = posts_api.create_post("temp", "for fixture demo", 1)
    post = resp.json()
    yield post
    posts_api.delete_post(post["id"])


def test_with_prepared_data(created_post):
    assert created_post["title"] == "temp"

"""
接口层（API Object 模式，和 UI 自动化里的 Page Object 是同一个思路）：
把「某个业务模块有哪些接口」封装成一个类。
用例只调用 posts_api.get_post(1)，不关心 URL 和请求细节。
接口地址变了只改这里，用例不用动。
"""
import allure

from common.http_client import HttpClient


class PostsApi:
    def __init__(self, client: HttpClient):
        self.client = client

    @allure.step("查询帖子 id={post_id}")
    def get_post(self, post_id):
        return self.client.get(f"/posts/{post_id}")

    @allure.step("按用户查询帖子 userId={user_id}")
    def list_posts_by_user(self, user_id):
        return self.client.get("/posts", params={"userId": user_id})

    @allure.step("创建帖子")
    def create_post(self, title, body, user_id):
        return self.client.post("/posts", json={"title": title, "body": body, "userId": user_id})

    @allure.step("修改帖子标题 id={post_id}")
    def update_title(self, post_id, title):
        return self.client.patch(f"/posts/{post_id}", json={"title": title})

    @allure.step("删除帖子 id={post_id}")
    def delete_post(self, post_id):
        return self.client.delete(f"/posts/{post_id}")

    @allure.step("查询帖子评论 id={post_id}")
    def list_comments(self, post_id):
        return self.client.get(f"/posts/{post_id}/comments")

"""用户模块接口（写法和 posts_api.py 一样，对照着看）。"""
import allure

from common.http_client import HttpClient


class UsersApi:
    def __init__(self, client: HttpClient):
        self.client = client

    @allure.step("查询所有用户")
    def list_users(self):
        return self.client.get("/users")

    @allure.step("查询用户 id={user_id}")
    def get_user(self, user_id):
        return self.client.get(f"/users/{user_id}")

    @allure.step("查询用户 {user_id} 的待办")
    def list_todos(self, user_id, completed=None):
        params = {"completed": str(completed).lower()} if completed is not None else None
        return self.client.get(f"/users/{user_id}/todos", params=params)

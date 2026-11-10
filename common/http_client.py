"""
对 requests 的二次封装。

为什么要封装：
1. base_url 只配一次，用例里只写 "/posts/1" 这种路径
2. 统一超时、公共 header
3. 每个请求/响应自动打日志，并附到 Allure 报告里，排查失败很方便
"""
import json
import logging

import allure
import requests

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, base_url: str, timeout: int = 15, headers: dict | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        # Session 会复用 TCP 连接，并自动保存 cookie（登录类接口常用）
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})
        if headers:
            self.session.headers.update(headers)

    def set_token(self, token: str):
        """接口关联示例：登录拿到 token 后调用，后续请求都会带上。"""
        self.session.headers["Authorization"] = f"Bearer {token}"

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        logger.info("请求: %s %s", method.upper(), url)
        if "json" in kwargs:
            logger.info("请求体: %s", kwargs["json"])

        resp = self.session.request(method, url, **kwargs)

        logger.info("响应: %s, 耗时 %.0f ms", resp.status_code, resp.elapsed.total_seconds() * 1000)
        self._attach_to_allure(method, url, kwargs, resp)
        return resp

    # 常用方法的快捷写法
    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)

    @staticmethod
    def _attach_to_allure(method, url, kwargs, resp):
        """把请求和响应挂到 Allure 报告的当前步骤上。"""
        req_info = {"method": method.upper(), "url": url,
                    "params": kwargs.get("params"), "json": kwargs.get("json")}
        allure.attach(json.dumps(req_info, ensure_ascii=False, indent=2),
                      name="Request", attachment_type=allure.attachment_type.JSON)
        allure.attach(resp.text, name=f"Response {resp.status_code}",
                      attachment_type=allure.attachment_type.TEXT)

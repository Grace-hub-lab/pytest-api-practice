"""
第 1 课：最基础的 pytest 写法（还没用框架封装，直接用 requests）。
先看懂这个文件，再看 test_02 / test_03 里封装后的写法，对比体会封装的好处。
"""
import requests

BASE = "https://jsonplaceholder.typicode.com"


def test_get_post_raw():
    """一条最原始的接口用例：发请求 -> 断言。"""
    resp = requests.get(f"{BASE}/posts/1", timeout=15)

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "title" in data


class TestGroupExample:
    """用 class 把相关用例分组，类名必须以 Test 开头，且不能写 __init__。"""

    def test_list_length(self):
        resp = requests.get(f"{BASE}/posts", timeout=15)
        assert len(resp.json()) == 100

    def test_filter_by_user(self):
        resp = requests.get(f"{BASE}/posts", params={"userId": 1}, timeout=15)
        # 列表推导 + all()：断言每一条都属于 userId=1
        assert all(p["userId"] == 1 for p in resp.json())

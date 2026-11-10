"""常用断言封装，让用例更简洁、报错信息更清楚。"""
import jsonschema

from common.file_loader import load_json
from common.paths import SCHEMA_DIR


def assert_status(resp, expected: int):
    assert resp.status_code == expected, (
        f"状态码不对: 期望 {expected}, 实际 {resp.status_code}, 响应: {resp.text[:300]}"
    )


def assert_fields(actual: dict, expected: dict):
    """逐个字段比较，只比 expected 里列出的字段（响应里多出来的字段不管）。"""
    for key, value in expected.items():
        assert key in actual, f"响应缺少字段 '{key}'"
        assert actual[key] == value, f"字段 '{key}': 期望 {value!r}, 实际 {actual[key]!r}"


def assert_schema(data, schema_file: str):
    """用 JSON Schema 校验响应结构（字段是否齐全、类型是否正确）。"""
    schema = load_json(SCHEMA_DIR / schema_file)
    jsonschema.validate(instance=data, schema=schema)

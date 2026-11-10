"""读取 YAML / JSON 文件的工具函数。"""
import json
from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    """读取 YAML 文件，返回 dict。encoding 指定 utf-8，避免中文乱码。"""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

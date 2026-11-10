"""统一管理项目路径，避免在各处写死相对路径。"""
from pathlib import Path

# 项目根目录 = 本文件的上两级（common/paths.py -> 项目根）
ROOT_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = ROOT_DIR / "config"
DATA_DIR = ROOT_DIR / "data"
SCHEMA_DIR = DATA_DIR / "schemas"

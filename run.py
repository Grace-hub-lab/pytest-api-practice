"""
一键运行入口：python run.py
等价于命令行 pytest，额外生成 HTML 报告和 Allure 原始数据。
"""
import sys

import pytest

if __name__ == "__main__":
    args = [
        "--html=reports/report.html",
        "--self-contained-html",
        "--alluredir=allure-results",
        "--clean-alluredir",
    ]
    # 透传命令行参数，例如：python run.py -m smoke --env=dev
    args += sys.argv[1:]
    sys.exit(pytest.main(args))

#!/usr/bin/python
# -*- coding: UTF-8 -*-
from utils.tool_data_time import DateTimeTool
import argparse
import pytest
import time
from loguru import logger
import subprocess
import os
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).parent

# 确保报告目录存在
report_dir = BASE_DIR / Path("test_report") / "report"
allure_report_dir = BASE_DIR / Path("test_report") / "allure_report"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='只执行匹配关键字的用例，会匹配文件名', type=str)
    parser.add_argument('-d', '--dir', help='指定要测试的目录', type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试', type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0', type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0', type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0', type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    parser.add_argument('-n', '--n', help='n是指定并发数', type=str)
    args = parser.parse_args()

    print('%s初始化基础数据......' % DateTimeTool.get_now_time())
    pass
    print('%s基础数据初始化完成......' % DateTimeTool.get_now_time())

    exit_code = 0
    # 此处加载运行参数配置：
    pytest_execute_params = [
        '-c', 'pytest.ini',
        '-v',
        f'--alluredir={report_dir}',
        '--clean-alluredir'  # 清理旧的测试结果
    ]

    # 判断目录参数
    case_dir = './test_cases/ehr/'
    if args.dir:
        case_dir = args.dir
    pytest_execute_params.append(case_dir)

    print('%s开始测试......' % DateTimeTool.get_now_time())
    t1 = time.time()

    # 执行测试并检查结果目录
    tmp_exit_code = pytest.main(pytest_execute_params)
    if not tmp_exit_code == 0:
        exit_code = tmp_exit_code
    
    # 检查是否生成了测试结果文件
    if not list(report_dir.glob('*')):
        print(f"警告: 在 {report_dir} 目录下未找到测试结果文件")
        print("请确保测试用例中正确使用了 Allure 装饰器")
        exit(1)

    t2 = time.time()

    print('%s结束测试......' % (DateTimeTool.get_now_time()))
    print('本次运行总耗时: %s s......' % (t2-t1))

    # 方式一:
    # os.system('allure generate ./test_report/report -o ./test_report/allure_report --clean')
    # os.system('allure open -h 127.0.0.1 -p 8883 ./test_report/allure_report')
    # 方式二:
    os.system('allure serve ./test_report/report')

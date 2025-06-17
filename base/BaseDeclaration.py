from pathlib import Path


BASE_DIR = Path(__file__).parent

allure_results_dir = BASE_DIR / Path("test_cases") / "report"
allure_report_dir = BASE_DIR / Path("test_cases") / "allure_report"
logs_dir = BASE_DIR / Path("test_reports")

# 响应枚举
SUCCESS_CODE = '200'
SUCCESS_MSG = 'success'

WARNING_TIME = 5

# 接口响应时间list，单位毫秒
STRESS_LIST = []

# 接口执行结果list
RESULT_LIST = []
import pytest
import yaml
import allure
from base.BaseAssert import Assertions
from apis.apis_ehr import ApiEhr
from loguru import logger
import os, sys
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.parent
CASE_DIR = Path("test_data") / "ehr_cases.yaml"

with open(BASE_DIR / CASE_DIR, 'r', encoding='utf-8') as f:
    test_data = yaml.safe_load(f)


@allure.epic("EHR接口测试")
@allure.feature("用户管理模块")
class TestUsers:
    def setup_class(self):
        self.api = ApiEhr()
        self.assertions = Assertions()

    @allure.story("用户登录")
    @allure.title("测试用户登录功能")
    @allure.description("测试用户登录功能")
    @pytest.mark.P0
    def test_login(self):
        with allure.step("1、用户登录成功"):
            login_data = test_data['user_module']['case1']['login']
            response = self.api.login(login_data)
        with allure.step("2、登录后获取token成功"):
            allure.attach(str(response), name='返回参数：')
            self.assertions.assert_code(response['status_code'], 200)
            self.assertions.assert_exist(response['extracted']["token"])

    @allure.story("用户查询")
    @allure.title("测试用户查询功能")
    @pytest.mark.P1
    def test_search_users(self):
        usernames = test_data['user_module']['case2']['search_user']['username']
        with allure.step("循环查询用户，查看查询结果是否正确"):
            for username in usernames:
                allure.attach(username, name='查询用户：')
                response = self.api.get_users(username=username)
                allure.attach(str(response), name='查询结果：')
                self.assertions.assert_code(response['status_code'], 300)
                self.assertions.assert_equal(response['extracted']["username"], username)

    @allure.story("用户管理")
    @allure.title("测试添加用户功能")
    @pytest.mark.P0
    @pytest.mark.正常系
    def test_add_user(self):
        '''
        1、新增用户，新增成功；
        2、新增的用户查询正确；
        :return:
        '''
        with allure.step("1、新增用户成功"):
            user_info = test_data['user_module']['case3-addUser']['userinfo']
            allure.attach(str(user_info), name='请求参数：')
            response1 = self.api.add_user(user_info=user_info)
            allure.attach(str(response1), name='新增结果：')
            self.assertions.assert_code(response1['status_code'], 200)
            self.assertions.assert_equal(response1['extracted']["username"], user_info['username'])

        with allure.step("2、新增用户后查询信息正确"):
            response2 = self.api.get_users(username=user_info['username'])
            allure.attach(str(response2), name='新增后查询：')
            self.assertions.assert_equal(response2['extracted']["username"], user_info['username'])


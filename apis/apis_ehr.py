import json
from base.BaseRequests import Request
from utils.get_api_info import get_apis
from business.get_token import get_common_header


class ApiEhr:
    def __init__(self):
        self.apis = get_apis(of_business="EHR")
        self.common_headers = get_common_header()
        self.req = Request()

    # 登录接口
    def login(self, user_info):
        api_info = (self.apis["登录接口"]).copy()
        api_info["req_body"] = user_info
        return self.req.common_req(api_info=api_info)

    # 查询用户信息
    def get_users(self, username):
        api_info = (self.apis["用户查询接口"]).copy()
        api_info["req_params"] = {"username": username}
        api_info["req_header"] = self.common_headers
        return self.req.common_req(api_info=api_info)


    # 新增用户信息
    def add_user(self, user_info):
        api_info = (self.apis["用户新增接口"]).copy()
        api_info["req_body"] = user_info
        api_info["req_header"] = self.common_headers
        return self.req.common_req(api_info=api_info)


if __name__ == '__main__':
    new_api = ApiEhr()
    s = new_api.add_user(user_info={"username": "testor1", "password": "123456", "phone": "13800138001"})
    print(s)
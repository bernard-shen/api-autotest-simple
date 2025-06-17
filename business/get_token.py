from base.BaseRequests import Request
from utils.get_api_info import get_api_info
from loguru import logger
import json

new_req = Request()
apis_info = get_api_info(of_business="EHR", api_name="登录接口")

def get_ehr_token(user_info):
    apis_info["req_body"] = user_info
    logger.info("\n" + "-" * 6 + "获取token...")
    res = new_req.common_req(api_info=apis_info)
    return res["extracted"]["token"]

def get_common_header():
    token = get_ehr_token(user_info={"username": "admin", "password": "123456"})
    common_headers = json.loads(apis_info["req_header"])
    common_headers.update({"authorization": token})
    return common_headers



if __name__ == '__main__':
    # token = get_ehr_token(user_info={"username": "testor", "password": "123456"})
    # print(token)
    headers = get_common_header()
    print("dsfasd %s", headers)
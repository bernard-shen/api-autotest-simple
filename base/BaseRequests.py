"""
封装request
"""

import os
import random
import requests
import json
from loguru import logger
from utils.get_extract_data import extract_data_from_response
from base.BaseDeclaration import logs_dir

logger.add(logs_dir, format="{time} {level} {message}", level="INFO")


class Request:

    def __init__(self):
        pass

    def common_req(self, api_info: dict):
        """
        通用请求方法，根据api_info组装请求并提取返回值
        """
        url = api_info.get('host', '') + api_info.get('api_path', '')
        method = api_info.get('req_method', 'GET').upper()
        headers = json.loads(api_info.get('req_header')) if isinstance(api_info.get('req_header'), str) else api_info.get('req_header')
        params = api_info.get('req_params')

        if params:
            params = json.loads(params) if isinstance(params, str) else params
        else:
            params = {}
        body = api_info.get('req_body')
        if body:
            body = json.loads(body) if isinstance(body, str) else body
        else:
            body = {}

        body_type = api_info.get('body_type', '').lower()
        # 组装请求参数
        request_args = {
            'url': url,
            'headers': headers
        }
        if method == 'GET':
            request_args['params'] = params or body
        elif method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if body_type == 'json':
                request_args['json'] = body
            elif body_type == 'form':
                request_args['data'] = body
            else:
                request_args['data'] = body
        # 发送请求
        logger.info("\n"+"-"*6+"请求参数为：{}".format(request_args))
        response = requests.request(method, **request_args)
        logger.info("\n"+"-"*6+"返回参数为：{}".format(response.json()))

        # 提取返回值
        extract_dict =  json.loads(api_info.get('extr_value'))
        # logger.info("\n"+"-"*6+"待提取值为：{}".format(extract_dict))

        if extract_dict:
            extract_dict = json.loads(extract_dict) if isinstance(extract_dict, str) else extract_dict
        else:
            extract_dict = {}
        extracted = extract_data_from_response(response.json(), extract_dict) if extract_dict else {}
        logger.info("\n"+"-"*6+"提取值内容为：{}".format(extracted))

        return {
            'status_code': response.status_code,
            'response': response.json(),
            'extracted': extracted
        }

    def get_request(self, url, header, data=None):
        try:
            if data is None:
                response = requests.get(url=url, headers=header)
                return response.json()
            else:
                response = requests.get(url=url, params=data, headers=header)
                return response.json()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()


    def post_request(self, url, data, header):
        pass


    def post_request_multipart(self, url, data, header, file_parm, file, f_type):
        """
        提交Multipart/form-data 格式的Post请求
        """
        pass

    def put_request(self, url, data, header):
        """
        Put请求
        """
        pass
    


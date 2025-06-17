"""
封装Assert方法，使断言更简洁明确
"""

import time
import json
from loguru import logger


# logger.add('../logs/mylogs/{}.txt'.format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())))


class Assertions:
    def __init__(self):
        self.log = logger

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert code == expected_code
            return True
        except:
            self.log.error("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))
            raise

    def assert_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            return True

        except:
            self.log.error("Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, body_msg))
            raise

    def assert_json(self, body, key, expected_json):
        """
        验证response body中某个第一层字段对应的json返回
        :param body:
        :param key:
        :param expected_json:
        :return:
        """
        try:
            real = json.loads(body)[key]
            assert real == json.loads(expected_json)
            return True

        except:
            self.log.error("Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, body_msg))
            raise

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            assert expected_msg in text
            return True
        except:
            self.log.error("Response body Does not contain expected_msg, expected_msg is %s" % expected_msg)
            raise

    def assert_equal(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg
            return True
        except:
            self.log.error("Response body != expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))
            raise

    def assert_time(self, time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param body:
        :param expected_time:
        :return:
        """
        try:
            assert time < expected_time
            return True

        except:
            self.log.error("Response time > expected_time, expected_time is %s, time is %s" % (expected_time, time))
            raise

    def assert_exist(self, msg):
        try:
            assert msg != ""
            return True
        except Ellipsis as e:
            self.log.error(e.args)
            raise
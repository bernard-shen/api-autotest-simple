#-*- coding: utf-8 -*-
from utils.db_connector import SQLiteConnector
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'db.sqlite3')


def get_api_info(of_business, api_name, db_path=db_path):
    """
    连接sqlite数据库，按业务和接口名查询api_info表，返回接口信息字典
    :param of_business: 业务名称
    :param api_name: 接口名称
    """
    db = SQLiteConnector(db_path)
    sql_command = f"""SELECT * FROM api_info WHERE of_business = '{of_business}' AND api_name = '{api_name}' AND is_deleted = 0"""

    result = db.execute_one(sql_command)
    if not result:
        return None

    # 获取字段名
    fields = [
        'id', 'env', 'of_business', 'host', 'api_name', 'api_path', 'req_method',
        'req_body', 'body_type', 'req_header', 'req_params', 'resp_demo',
        'extr_value'
    ]
    return dict(zip(fields, result))


def get_apis(of_business, db_path=db_path):
    """
    连接sqlite数据库，按业务和接口名查询api_info表，返回接口信息字典
    :param of_business: 业务名称
    :param api_name: 接口名称
    """
    db = SQLiteConnector(db_path)

    sql_command = f"""SELECT * FROM api_info WHERE of_business = '{of_business}' AND is_deleted = 0"""


    result = db.execute_query(sql_command)
    if not result:
        return None
    tmp = {}
    # 获取字段名
    fields = [
        'id', 'env', 'of_business', 'host', 'api_name', 'api_path', 'req_method',
        'req_body', 'body_type', 'req_header', 'req_params', 'resp_demo',
        'extr_value'
    ]
    for row in result:
        tmp[row[4]] = dict(zip(fields, row))
    return tmp


if __name__ == '__main__':
    print(get_apis(of_business="EHR"))

import json
from typing import Any, Dict
from jsonpath_ng import parse as jsonpath_parse

def extract_data_from_response(response: Dict[str, Any], jsonpath_dict: Dict[str, str]) -> Dict[str, Any]:
    """
    根据jsonpath_dict中的jsonpath表达式，从response中提取对应的值。
    Args:
        response (Dict[str, Any]): 接口返回的字典
        jsonpath_dict (Dict[str, str]): 形如{"username": "$.data.username", "phone": "$data.info[0].phone"}
    Returns:
        Dict[str, Any]: 提取后的字典
    """
    result = {}
    for key, json_path in jsonpath_dict.items():
        try:
            jsonpath_expr = jsonpath_parse(json_path)
            match = jsonpath_expr.find(response)
            result[key] = match[0].value if match else None
        except Exception as e:
            result[key] = None
    return result

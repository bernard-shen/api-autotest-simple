from typing import Any, Dict, Optional, List, Union
import pandas as pd
import os
import json
import yaml



class YamlData:
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        self.data = self._load_yaml()

    def _load_yaml(self) -> Dict:
        if not os.path.exists(self.yaml_path):
            raise FileNotFoundError(f"文件找不到: {self.yaml_path}")
            
        try:
            with open(self.yaml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"文件解析错误，请确认文件格式: {str(e)}")

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        value = self.data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_by_parent_child(self, parent: str, child: Optional[str] = None, default: Any = None) -> Union[Dict, Any]:
        """
        使用parent和child的形式获取嵌套数据
        
        Args:
            parent (str): 父级key
            child (str, optional): 子级key，如果不指定则返回父级下的所有数据
            default (Any, optional): 默认值，当数据不存在时返回
            
        Returns:
            Union[Dict, Any]: 返回获取到的数据，如果指定了child则返回具体值，否则返回字典
        """
        parent_data = self.get(parent, {})
        if not isinstance(parent_data, dict):
            return default
            
        if child is None:
            return parent_data
            
        return parent_data.get(child, default)

    def get_dict(self, key_path: str) -> Dict:
        value = self.get(key_path, {})
        return value if isinstance(value, dict) else {}

    def get_list(self, key_path: str) -> list:
        value = self.get(key_path, [])
        return value if isinstance(value, list) else []


class ExcelData:
    def __init__(self, excel_path: str, sheet_name: Optional[Union[str, int]] = 0):
        """
        初始化Excel数据读取类
        
        Args:
            excel_path (str): Excel文件路径
            sheet_name (Union[str, int], optional): 工作表名称或索引，默认为第一个工作表
        """
        self.excel_path = excel_path
        self.sheet_name = sheet_name
        self.df = self._load_excel()

    def _load_excel(self) -> pd.DataFrame:
        """
        加载Excel文件
        
        Returns:
            pd.DataFrame: 加载的Excel数据
        """
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(f"Excel文件找不到: {self.excel_path}")
            
        try:
            return pd.read_excel(self.excel_path, sheet_name=self.sheet_name)
        except Exception as e:
            raise ValueError(f"Excel文件读取错误: {str(e)}")

    def get_all_data(self) -> List[Dict]:
        """
        获取所有行数据，返回嵌套列表字典形式
        
        Returns:
            List[Dict]: 包含所有行数据的列表，每行数据以字典形式存储
        """
        # 将DataFrame转换为字典列表，处理NaN值
        data = self.df.replace({pd.NA: None}).to_dict('records')
        return data

    def get_row_by_case_name(self, case_name: str) -> Optional[Dict]:
        """
        根据用例名称获取一行数据
        
        Args:
            case_name (str): 用例名称
            
        Returns:
            Optional[Dict]: 返回匹配的行数据，如果未找到则返回None
        """
        # 假设用例名称在'case_name'列，如果不是，需要修改列名
        if 'case_name' not in self.df.columns:
            raise ValueError("Excel文件中未找到'case_name'列")
            
        row = self.df[self.df['case_name'] == case_name]
        if row.empty:
            return None
            
        # 将匹配的行转换为字典，处理NaN值
        return row.replace({pd.NA: None}).to_dict('records')[0]

    def get_row_by_id(self, case_id: Union[str, int]) -> Optional[Dict]:
        """
        根据用例ID获取一行数据
        
        Args:
            case_id (Union[str, int]): 用例ID
            
        Returns:
            Optional[Dict]: 返回匹配的行数据，如果未找到则返回None
        """
        # 假设用例ID在'case_id'列，如果不是，需要修改列名
        if 'case_id' not in self.df.columns:
            raise ValueError("Excel文件中未找到'case_id'列")
            
        row = self.df[self.df['case_id'] == case_id]
        if row.empty:
            return None
            
        # 将匹配的行转换为字典，处理NaN值
        return row.replace({pd.NA: None}).to_dict('records')[0]


class JsonData:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = self._load_json()

    def _load_json(self) -> Dict:
        """
        加载JSON文件
        
        Returns:
            Dict: 加载的JSON数据
        """
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"JSON文件找不到: {self.json_path}")
            
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON文件解析错误: {str(e)}")

    def get_all_data(self) -> Dict:
        return self.data

    def get_data_by_key(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def get_nested_data(self, key_path: str, default: Any = None) -> Any:
        """
        获取嵌套数据，支持使用点号分隔的路径
        
        Args:
            key_path (str): 使用点号分隔的key路径，例如 'parent.child.key'
            default (Any, optional): 默认值，当路径不存在时返回
            
        Returns:
            Any: 返回路径对应的数据，如果路径不存在则返回默认值
        """
        keys = key_path.split('.')
        value = self.data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

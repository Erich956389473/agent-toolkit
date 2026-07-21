"""Validator模块的Python实现"""

import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    errors: List[str]
    warnings: List[str]


class Validator:
    """Agent Card验证器"""
    
    def __init__(self):
        """初始化验证器"""
        # 定义必填字段
        self.required_fields = ["name", "url"]
        
        # 定义字段格式
        self.field_formats = {
            "name": {"type": "string", "min_length": 1, "max_length": 100},
            "url": {"type": "string", "format": "uri"},
            "description": {"type": "string", "max_length": 1000},
            "version": {"type": "string", "pattern": r"^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$"},
        }
    
    def validate(self, card: Dict[str, Any]) -> ValidationResult:
        """验证Agent Card"""
        errors = []
        warnings = []
        
        # 检查是否为字典
        if not isinstance(card, dict):
            return ValidationResult(
                valid=False,
                errors=["Card must be a JSON object"],
                warnings=[]
            )
        
        # 检查必填字段
        for field in self.required_fields:
            if field not in card:
                errors.append(f"Missing required field: {field}")
            elif not card[field]:
                errors.append(f"Field '{field}' cannot be empty")
        
        # 检查字段格式
        for field, rules in self.field_formats.items():
            if field in card:
                value = card[field]
                
                # 检查类型（字符串比较）
                if "type" in rules:
                    expected_type = rules["type"]
                    actual_type = type(value).__name__
                    if expected_type == "string" and not isinstance(value, str):
                        errors.append(f"Field '{field}' must be of type {expected_type}")
                        continue
                    elif expected_type == "number" and not isinstance(value, (int, float)):
                        errors.append(f"Field '{field}' must be of type {expected_type}")
                        continue
                    elif expected_type == "boolean" and not isinstance(value, bool):
                        errors.append(f"Field '{field}' must be of type {expected_type}")
                        continue
                
                # 检查字符串长度
                if isinstance(value, str):
                    if "min_length" in rules and len(value) < rules["min_length"]:
                        errors.append(f"Field '{field}' must be at least {rules['min_length']} characters")
                    if "max_length" in rules and len(value) > rules["max_length"]:
                        errors.append(f"Field '{field}' must be at most {rules['max_length']} characters")
                
                # 检查URL格式
                if field == "url" and "format" in rules and rules["format"] == "uri":
                    if not self._is_valid_url(value):
                        errors.append(f"Field '{field}' must be a valid URL")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_json(self, json_str: str) -> ValidationResult:
        """验证JSON字符串"""
        try:
            card = json.loads(json_str)
            return self.validate(card)
        except json.JSONDecodeError as e:
            return ValidationResult(
                valid=False,
                errors=[f"Invalid JSON: {str(e)}"],
                warnings=[]
            )
    
    def validate_file(self, file_path: str) -> ValidationResult:
        """验证JSON文件"""
        if not os.path.exists(file_path):
            return ValidationResult(
                valid=False,
                errors=[f"File not found: {file_path}"],
                warnings=[]
            )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.validate_json(content)
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Error reading file: {str(e)}"],
                warnings=[]
            )
    
    def _is_valid_url(self, url: str) -> bool:
        """简单的URL验证"""
        return url.startswith(('http://', 'https://')) and '.' in url
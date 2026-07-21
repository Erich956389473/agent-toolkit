"""Validator模块的Python测试（使用unittest）"""

import unittest
import json
import tempfile
import os
from validator import Validator, ValidationResult


class TestValidator(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.validator = Validator()
        
        # 有效的Agent Card
        self.valid_card = {
            "name": "Test Agent",
            "url": "https://example.com/agent",
            "description": "A test agent",
            "version": "1.0.0"
        }
        
        # 无效的Agent Card（缺少必填字段）
        self.invalid_card = {
            "description": "Missing name and url fields"
        }
    
    def test_new_validator(self):
        """测试创建Validator实例"""
        v = Validator()
        self.assertIsNotNone(v)
    
    def test_validate_valid_card(self):
        """验证有效Card"""
        result = self.validator.validate(self.valid_card)
        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_validate_invalid_card(self):
        """验证无效Card（缺少必填字段）"""
        result = self.validator.validate(self.invalid_card)
        self.assertFalse(result.valid)
        self.assertGreater(len(result.errors), 0)
        # 检查错误信息是否包含缺少的字段
        error_str = ' '.join(result.errors)
        self.assertIn("name", error_str.lower())
        self.assertIn("url", error_str.lower())
    
    def test_validate_json_string(self):
        """验证JSON字符串"""
        valid_json = json.dumps(self.valid_card)
        result = self.validator.validate_json(valid_json)
        self.assertTrue(result.valid)
        
        invalid_json = json.dumps(self.invalid_card)
        result = self.validator.validate_json(invalid_json)
        self.assertFalse(result.valid)
    
    def test_validate_file(self):
        """验证JSON文件"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_card, f)
            temp_path = f.name
        
        try:
            result = self.validator.validate_file(temp_path)
            self.assertTrue(result.valid)
        finally:
            os.unlink(temp_path)
    
    def test_validation_result_format(self):
        """验证结果格式"""
        result = self.validator.validate(self.valid_card)
        
        # 检查结果属性
        self.assertTrue(hasattr(result, 'valid'))
        self.assertTrue(hasattr(result, 'errors'))
        self.assertTrue(hasattr(result, 'warnings'))
        
        # 检查类型
        self.assertIsInstance(result.valid, bool)
        self.assertIsInstance(result.errors, list)
        self.assertIsInstance(result.warnings, list)


if __name__ == "__main__":
    unittest.main()
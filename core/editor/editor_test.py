"""Editor模块的Python测试（使用unittest）"""

import unittest
import json
import tempfile
import os
from editor import Editor, AgentCard


class TestEditor(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.editor = Editor()
        
        # 有效的Agent Card
        self.valid_card = AgentCard(
            name="Test Agent",
            url="https://example.com/agent",
            description="A test agent",
            version="1.0.0"
        )
    
    def test_new_editor(self):
        """测试创建Editor实例"""
        e = Editor()
        self.assertIsNotNone(e)
        self.assertEqual(len(e.list()), 0)
    
    def test_create_card(self):
        """测试创建Card"""
        card_id = self.editor.create(self.valid_card)
        self.assertIsNotNone(card_id)
        self.assertIsInstance(card_id, str)
        
        # 检查Card是否已创建
        cards = self.editor.list()
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0].name, "Test Agent")
    
    def test_update_card(self):
        """测试更新Card"""
        card_id = self.editor.create(self.valid_card)
        
        # 更新Card
        updated_card = AgentCard(
            name="Updated Agent",
            url="https://example.com/updated",
            description="Updated description",
            version="2.0.0"
        )
        self.editor.update(card_id, updated_card)
        
        # 检查更新结果
        card = self.editor.get(card_id)
        self.assertEqual(card.name, "Updated Agent")
        self.assertEqual(card.version, "2.0.0")
    
    def test_delete_card(self):
        """测试删除Card"""
        card_id = self.editor.create(self.valid_card)
        self.assertEqual(len(self.editor.list()), 1)
        
        self.editor.delete(card_id)
        self.assertEqual(len(self.editor.list()), 0)
        
        # 尝试获取已删除的Card
        card = self.editor.get(card_id)
        self.assertIsNone(card)
    
    def test_get_card(self):
        """测试获取Card"""
        card_id = self.editor.create(self.valid_card)
        
        card = self.editor.get(card_id)
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "Test Agent")
        self.assertEqual(card.url, "https://example.com/agent")
    
    def test_list_cards(self):
        """测试列出所有Card"""
        # 创建多个Card
        card1 = AgentCard(name="Agent 1", url="https://example.com/1")
        card2 = AgentCard(name="Agent 2", url="https://example.com/2")
        card3 = AgentCard(name="Agent 3", url="https://example.com/3")
        
        id1 = self.editor.create(card1)
        id2 = self.editor.create(card2)
        id3 = self.editor.create(card3)
        
        cards = self.editor.list()
        self.assertEqual(len(cards), 3)
        
        # 检查Card名称
        names = [card.name for card in cards]
        self.assertIn("Agent 1", names)
        self.assertIn("Agent 2", names)
        self.assertIn("Agent 3", names)
    
    def test_get_non_existent_card(self):
        """测试获取不存在的Card"""
        card = self.editor.get("non-existent-id")
        self.assertIsNone(card)
    
    def test_delete_non_existent_card(self):
        """测试删除不存在的Card（不应报错）"""
        try:
            self.editor.delete("non-existent-id")
        except Exception as e:
            self.fail(f"delete raised {e} unexpectedly")
    
    def test_update_non_existent_card(self):
        """测试更新不存在的Card（不应报错）"""
        card = AgentCard(name="Ghost", url="https://example.com/ghost")
        try:
            self.editor.update("non-existent-id", card)
        except Exception as e:
            self.fail(f"update raised {e} unexpectedly")
    
    def test_export_json(self):
        """测试导出Card为JSON"""
        card_id = self.editor.create(self.valid_card)
        json_str = self.editor.export_json(card_id)
        self.assertIsNotNone(json_str)
        data = json.loads(json_str)
        self.assertEqual(data["name"], "Test Agent")
    
    def test_import_json(self):
        """测试从JSON导入Card"""
        json_str = '{"name": "Imported", "url": "https://example.com/imported"}'
        card_id = self.editor.import_json(json_str)
        self.assertIsNotNone(card_id)
        card = self.editor.get(card_id)
        self.assertEqual(card.name, "Imported")
    
    def test_import_invalid_json(self):
        """测试导入无效JSON"""
        result = self.editor.import_json("invalid json")
        self.assertIsNone(result)
    
    def test_export_non_existent_card(self):
        """测试导出不存在的Card"""
        result = self.editor.export_json("non-existent-id")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
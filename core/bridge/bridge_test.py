"""Bridge模块的Python测试（使用unittest）"""

import unittest
import asyncio
from bridge import Bridge, Message, Adapter, MockAdapter


class TestBridge(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.bridge = Bridge()
    
    def test_new_bridge(self):
        """测试创建Bridge实例"""
        b = Bridge()
        self.assertIsNotNone(b)
        self.assertEqual(len(b.get_supported_protocols()), 0)
    
    def test_register_adapter(self):
        """测试注册协议适配器"""
        mock_adapter = MockAdapter(protocol="test")
        self.bridge.register_adapter("test", mock_adapter)
        
        protocols = self.bridge.get_supported_protocols()
        self.assertIn("test", protocols)
        self.assertEqual(len(protocols), 1)
    
    def test_send_message(self):
        """测试发送消息"""
        mock_adapter = MockAdapter(protocol="test")
        self.bridge.register_adapter("test", mock_adapter)
        
        message = Message(
            from_agent="agent1",
            to_agent="test:agent2",
            content="Hello"
        )
        
        # 发送消息
        asyncio.run(self.bridge.send(message))
        
        # 检查适配器是否收到消息
        self.assertEqual(len(mock_adapter.sent_messages), 1)
        self.assertEqual(mock_adapter.sent_messages[0].content, "Hello")
    
    def test_receive_message(self):
        """测试接收消息"""
        mock_adapter = MockAdapter(protocol="test")
        self.bridge.register_adapter("test", mock_adapter)
        
        # 模拟接收消息
        test_message = Message(
            from_agent="agent1",
            to_agent="agent2",
            content="Test message"
        )
        mock_adapter.add_incoming_message(test_message)
        
        async def test_receive():
            messages = []
            async for msg in self.bridge.receive():
                messages.append(msg)
                if len(messages) >= 1:
                    break
            return messages
        
        messages = asyncio.run(test_receive())
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, "Test message")
    
    def test_multiple_protocols(self):
        """测试多协议支持"""
        adapter1 = MockAdapter(protocol="mcp")
        adapter2 = MockAdapter(protocol="a2a")
        
        self.bridge.register_adapter("mcp", adapter1)
        self.bridge.register_adapter("a2a", adapter2)
        
        protocols = self.bridge.get_supported_protocols()
        self.assertEqual(len(protocols), 2)
        self.assertIn("mcp", protocols)
        self.assertIn("a2a", protocols)
    
    def test_message_routing(self):
        """测试消息路由"""
        mcp_adapter = MockAdapter(protocol="mcp")
        a2a_adapter = MockAdapter(protocol="a2a")
        
        self.bridge.register_adapter("mcp", mcp_adapter)
        self.bridge.register_adapter("a2a", a2a_adapter)
        
        # 发送MCP消息
        mcp_message = Message(
            from_agent="agent1",
            to_agent="mcp:server1",
            content="MCP message"
        )
        asyncio.run(self.bridge.send(mcp_message))
        
        # 发送A2A消息
        a2a_message = Message(
            from_agent="agent1",
            to_agent="a2a:agent2",
            content="A2A message"
        )
        asyncio.run(self.bridge.send(a2a_message))
        
        # 检查消息路由
        self.assertEqual(len(mcp_adapter.sent_messages), 1)
        self.assertEqual(len(a2a_adapter.sent_messages), 1)
        self.assertEqual(mcp_adapter.sent_messages[0].content, "MCP message")
        self.assertEqual(a2a_adapter.sent_messages[0].content, "A2A message")
    
    def test_send_to_unknown_protocol(self):
        """测试发送到未注册的协议"""
        message = Message(from_agent="agent1", to_agent="unknown:target", content="Hello")
        with self.assertRaises(ValueError):
            asyncio.run(self.bridge.send(message))
    
    def test_send_empty_message(self):
        """测试发送空消息"""
        mock_adapter = MockAdapter(protocol="test")
        self.bridge.register_adapter("test", mock_adapter)
        message = Message(from_agent="", to_agent="test:target", content="")
        asyncio.run(self.bridge.send(message))
        self.assertEqual(len(mock_adapter.sent_messages), 1)
    
    def test_register_multiple_adapters_same_protocol(self):
        """测试重复注册同一协议（覆盖旧适配器）"""
        adapter1 = MockAdapter(protocol="test")
        adapter2 = MockAdapter(protocol="test")
        self.bridge.register_adapter("test", adapter1)
        self.bridge.register_adapter("test", adapter2)
        protocols = self.bridge.get_supported_protocols()
        self.assertEqual(len(protocols), 1)  # 应该只保留最后一个


if __name__ == "__main__":
    unittest.main()
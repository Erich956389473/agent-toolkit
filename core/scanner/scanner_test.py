"""Scanner模块的Python测试（使用unittest）"""

import unittest
import asyncio
from scanner import Scanner, MockScanner


class TestScanner(unittest.TestCase):
    def test_new_scanner(self):
        """测试创建Scanner实例"""
        s = Scanner()
        self.assertIsNotNone(s)
    
    def test_scanner_scan(self):
        """测试Scan方法"""
        s = Scanner()
        agents = s.scan()
        self.assertIsInstance(agents, list)
        self.assertEqual(len(agents), 0)  # 初始状态应该为空
    
    def test_scanner_watch(self):
        """测试Watch方法"""
        s = Scanner()
        
        async def test_watch():
            events = []
            # 只运行0.3秒，避免无限循环
            async for event in s.watch(timeout=0.1):
                events.append(event)
                if len(events) >= 2:  # 最多获取2个事件
                    break
            return events
        
        events = asyncio.run(test_watch())
        # 初始状态应该至少有一个事件（添加mock agent）
        self.assertGreaterEqual(len(events), 1)
    
    def test_mock_scanner(self):
        """测试MockScanner"""
        mock = MockScanner(
            agents=[
                {
                    "id": "test-agent-1",
                    "name": "Test Agent",
                    "type": "test",
                    "status": "running",
                    "pid": 12345,
                }
            ]
        )
        
        agents = mock.scan()
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0]["id"], "test-agent-1")
    
    def test_scanner_add_agent(self):
        """测试添加Agent"""
        s = Scanner()
        agent = {
            "id": "test-agent-2",
            "name": "Test Agent 2",
            "type": "test",
            "status": "running",
            "pid": 12346,
        }
        s.add_agent(agent)
        
        agents = s.scan()
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0]["id"], "test-agent-2")
    
    def test_scanner_remove_agent(self):
        """测试移除Agent"""
        s = Scanner()
        agent = {
            "id": "test-agent-3",
            "name": "Test Agent 3",
            "type": "test",
            "status": "running",
            "pid": 12347,
        }
        s.add_agent(agent)
        s.remove_agent("test-agent-3")
        
        agents = s.scan()
        self.assertEqual(len(agents), 0)


if __name__ == "__main__":
    unittest.main()
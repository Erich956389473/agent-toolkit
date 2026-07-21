"""Scanner模块的Python实现"""

import asyncio
import time
from typing import List, Dict, Any, AsyncGenerator, Optional


class Scanner:
    """Scanner接口的Python实现"""
    
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
    
    def scan(self) -> List[Dict[str, Any]]:
        """扫描所有本地Agent"""
        return list(self.agents.values())
    
    async def watch(self, timeout: float = 1.0) -> AsyncGenerator[Dict[str, Any], None]:
        """监控Agent变化"""
        # 只运行一次，模拟添加一个agent后退出
        await asyncio.sleep(timeout)
        
        # 模拟扫描变化
        if len(self.agents) == 0:
            # 模拟添加一个Agent
            agent = {
                "id": "mock-agent-1",
                "name": "Mock Agent",
                "type": "mock",
                "status": "running",
                "pid": 12345,
                "command_line": "mock-agent --config config.yaml",
                "started_at": time.time(),
                "metadata": {"version": "1.0.0"},
            }
            
            self.agents[agent["id"]] = agent
            
            yield {
                "type": "add",
                "agent": agent,
            }
    
    def add_agent(self, agent: Dict[str, Any]) -> None:
        """添加一个Agent"""
        self.agents[agent["id"]] = agent
    
    def remove_agent(self, agent_id: str) -> None:
        """移除一个Agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取一个Agent"""
        return self.agents.get(agent_id)


class MockScanner:
    """模拟的Scanner实现"""
    
    def __init__(self, agents: List[Dict[str, Any]] = None):
        self.agents = agents or []
    
    def scan(self) -> List[Dict[str, Any]]:
        """返回模拟的Agent列表"""
        return self.agents
    
    async def watch(self, timeout: float = 1.0) -> AsyncGenerator[Dict[str, Any], None]:
        """模拟监控"""
        while True:
            await asyncio.sleep(timeout)
            # 模拟事件
            for agent in self.agents:
                yield {
                    "type": "update",
                    "agent": agent,
                }
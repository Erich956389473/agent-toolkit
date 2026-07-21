"""Bridge模块的Python实现"""

import asyncio
from typing import Dict, List, AsyncGenerator, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Message:
    """消息数据类"""
    from_agent: str
    to_agent: str
    content: str
    metadata: Optional[Dict[str, str]] = None


class Adapter(ABC):
    """协议适配器抽象基类"""
    
    @abstractmethod
    def get_protocol(self) -> str:
        """获取协议名称"""
        pass
    
    @abstractmethod
    async def send(self, message: Message) -> None:
        """发送消息"""
        pass
    
    @abstractmethod
    async def receive(self) -> AsyncGenerator[Message, None]:
        """接收消息"""
        pass


class MockAdapter(Adapter):
    """模拟适配器（用于测试）"""
    
    def __init__(self, protocol: str = "mock"):
        self.protocol = protocol
        self.sent_messages: List[Message] = []
        self.incoming_messages: List[Message] = []
    
    def get_protocol(self) -> str:
        return self.protocol
    
    async def send(self, message: Message) -> None:
        self.sent_messages.append(message)
    
    async def receive(self) -> AsyncGenerator[Message, None]:
        for message in self.incoming_messages:
            yield message
        self.incoming_messages.clear()
    
    def add_incoming_message(self, message: Message) -> None:
        """添加模拟的入站消息"""
        self.incoming_messages.append(message)


class Bridge:
    """Agent通信桥接器"""
    
    def __init__(self):
        self.adapters: Dict[str, Adapter] = {}
    
    def register_adapter(self, protocol: str, adapter: Adapter) -> None:
        """注册协议适配器"""
        self.adapters[protocol] = adapter
    
    def get_supported_protocols(self) -> List[str]:
        """获取支持的协议列表"""
        return list(self.adapters.keys())
    
    def _parse_destination(self, destination: str) -> tuple[str, str]:
        """解析目标地址，返回(协议, 目标)"""
        parts = destination.split(":", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return "", destination
    
    async def send(self, message: Message) -> None:
        """发送消息"""
        protocol, target = self._parse_destination(message.to_agent)
        
        if protocol not in self.adapters:
            raise ValueError(f"No adapter found for protocol: {protocol}")
        
        adapter = self.adapters[protocol]
        # 更新消息目标为解析后的目标
        updated_message = Message(
            from_agent=message.from_agent,
            to_agent=target,
            content=message.content,
            metadata=message.metadata
        )
        await adapter.send(updated_message)
    
    async def receive(self) -> AsyncGenerator[Message, None]:
        """接收所有适配器的消息"""
        # 依次从每个适配器接收消息
        for protocol, adapter in self.adapters.items():
            async for message in adapter.receive():
                yield message
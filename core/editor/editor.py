"""Editor模块的Python实现"""

import uuid
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class AgentCard:
    """Agent Card数据类"""
    name: str
    url: str
    description: str = ""
    version: str = "1.0.0"
    icon_url: str = ""
    provider_organization: str = ""
    provider_url: str = ""
    capabilities: List[str] = None
    default_input_modes: List[str] = None
    default_output_modes: List[str] = None
    skills: List[Dict] = None
    
    def __post_init__(self):
        """初始化默认值"""
        if self.capabilities is None:
            self.capabilities = []
        if self.default_input_modes is None:
            self.default_input_modes = []
        if self.default_output_modes is None:
            self.default_output_modes = []
        if self.skills is None:
            self.skills = []


class Editor:
    """Agent Card编辑器"""
    
    def __init__(self):
        """初始化编辑器"""
        self.cards: Dict[str, AgentCard] = {}
    
    def create(self, card: AgentCard) -> str:
        """创建新的Agent Card"""
        card_id = str(uuid.uuid4())
        self.cards[card_id] = card
        return card_id
    
    def update(self, card_id: str, card: AgentCard) -> None:
        """更新Agent Card"""
        if card_id in self.cards:
            self.cards[card_id] = card
    
    def delete(self, card_id: str) -> None:
        """删除Agent Card"""
        if card_id in self.cards:
            del self.cards[card_id]
    
    def get(self, card_id: str) -> Optional[AgentCard]:
        """获取Agent Card"""
        return self.cards.get(card_id)
    
    def list(self) -> List[AgentCard]:
        """列出所有Agent Card"""
        return list(self.cards.values())
    
    def export_json(self, card_id: str) -> Optional[str]:
        """导出Card为JSON字符串"""
        card = self.get(card_id)
        if card:
            import json
            return json.dumps(asdict(card), indent=2, ensure_ascii=False)
        return None
    
    def import_json(self, json_str: str) -> Optional[str]:
        """从JSON字符串导入Card"""
        try:
            import json
            data = json.loads(json_str)
            card = AgentCard(**data)
            return self.create(card)
        except Exception:
            return None
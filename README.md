[English](./README_EN.md) | 中文

---

# Agent Toolkit

> 一套完整的AI Agent开 发、管理和监控工具集。
> A complet e set of tools for AI Agent development, mana gement, and monitoring.

[![CI](https://githu b.com/Erich956389473/agent-toolkit/actions/wo rkflows/ci.yml/badge.svg)](https://github.com /Erich956389473/agent-toolkit/actions/workflo ws/ci.yml)
[![Python](https://img.shields.io/ badge/Python-3.10+-blue.svg)](https://www.pyt hon.org/)
[![Go](https://img.shields.io/badge /Go-1.21+-00ADD8.svg)](https://go.dev/)
[![Li cense](https://img.shields.io/badge/License-M IT-green.svg)](LICENSE)
[![GitHub Stars](http s://img.shields.io/github/stars/Erich95638947 3/agent-toolkit?style=social)](https://github .com/Erich956389473/agent-toolkit)

## 🎯 � ��目定位

Agent Toolkit 是一个统一的 工具套件，整合了四个核心工具： 
- **agent-inventory** - 本地AI Agent扫描 和发现
- **agent-card-editor** - A2A Agent  Card可视化编辑
- **agent-card-validator ** - A2A Agent Card规范验证
- **agent-bri dge** - Agent间通信桥接

## 🏗️ 架� ��设计

```
agent-toolkit/
├── cli/                   # 统一CLI入口
│   ├� �─ go/              # Go实现（高性能� ��
│   ├── python/          # Python� ��现（易用性）
│   └── rust/             # Rust实现（极致性能）
├� �─ core/                # 核心逻辑模� �
│   ├── scanner/         # Agent扫 描器
│   ├── editor/          # Car d编辑器
│   ├── validator/       #  Card验证器
│   └── bridge/           # 通信桥接器
├── web/                  # Web界面
│   ├── dashboard/        # 监控仪表盘
│   ├── edit or/          # 在线编辑器
│   └─� � docs/            # 文档站点
└── p lugins/             # 插件系统
    ├─ ─ mcp-adapter/     # MCP协议适配器
     ├── a2a-adapter/     # A2A协议适配 器
    └── http-adapter/    # HTTP协� ��适配器
```

## 🚀 快速开始

### � �装

```bash
# 使用Go版本（推荐）
go  install github.com/agent-toolkit/cli@latest
 
# 使用Python版本
pip install agent-toolk it

# 使用Rust版本
cargo install agent-to olkit
```

### 基本使用

```bash
# 扫描 本地Agent
agent-toolkit scan

# 编辑Agent  Card
agent-toolkit card edit

# 验证Agent  Card
agent-toolkit card validate my-card.json 

# 启动通信桥接
agent-toolkit bridge s tart
```

## 📦 核心功能

### 1. Agent� ��描与发现
- 跨平台进程扫描
- MCP� ��务器检测
- 实时状态监控
- 告警� ��知

### 2. Agent Card管理
- 可视化编 辑器
- JSON Schema验证
- 模板库
- 版� ��控制

### 3. 通信桥接
- 多协议支� ��（MCP、A2A、HTTP、WebSocket）
- 统一 消息格式
- 负载均衡
- 服务发现

# ## 4. 监控与日志
- 性能指标收集
-  错误日志分析
- 趋势可视化
- 告警 规则引擎

## 🛠️ 开发指南

### � �献新语言实现

我们欢迎用任何语 言实现核心功能：

1. 克隆仓库
2.  在 `cli/` 下创建新语言目录
3. 实现 核心接口
4. 添加测试
5. 提交PR

###  核心接口

```go
// Go接口定义
type S canner interface {
    Scan() ([]Agent, error )
    Watch(ctx context.Context) (<-chan Agen tEvent, error)
}

type Validator interface {
     Validate(card *AgentCard) (*ValidationRes ult, error)
    ValidateFile(path string) (*V alidationResult, error)
}
```

## 📚 文档 

- [架构设计](docs/architecture.md)
- [A PI参考](docs/api.md)
- [贡献指南](CONTR IBUTING.md)
- [更新日志](CHANGELOG.md)

# # 📄 许可证

MIT License 
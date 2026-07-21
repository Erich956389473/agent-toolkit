# Agent Toolkit

> 一套完整的AI Agent开发、管理和监控工具集。
> A complete set of tools for AI Agent development, management, and monitoring.

## 🎯 项目定位

Agent Toolkit 是一个统一的工具套件，整合了四个核心工具：
- **agent-inventory** - 本地AI Agent扫描和发现
- **agent-card-editor** - A2A Agent Card可视化编辑
- **agent-card-validator** - A2A Agent Card规范验证
- **agent-bridge** - Agent间通信桥接

## 🏗️ 架构设计

```
agent-toolkit/
├── cli/                  # 统一CLI入口
│   ├── go/              # Go实现（高性能）
│   ├── python/          # Python实现（易用性）
│   └── rust/            # Rust实现（极致性能）
├── core/                # 核心逻辑模块
│   ├── scanner/         # Agent扫描器
│   ├── editor/          # Card编辑器
│   ├── validator/       # Card验证器
│   └── bridge/          # 通信桥接器
├── web/                 # Web界面
│   ├── dashboard/       # 监控仪表盘
│   ├── editor/          # 在线编辑器
│   └── docs/            # 文档站点
└── plugins/             # 插件系统
    ├── mcp-adapter/     # MCP协议适配器
    ├── a2a-adapter/     # A2A协议适配器
    └── http-adapter/    # HTTP协议适配器
```

## 🚀 快速开始

### 安装

```bash
# 使用Go版本（推荐）
go install github.com/agent-toolkit/cli@latest

# 使用Python版本
pip install agent-toolkit

# 使用Rust版本
cargo install agent-toolkit
```

### 基本使用

```bash
# 扫描本地Agent
agent-toolkit scan

# 编辑Agent Card
agent-toolkit card edit

# 验证Agent Card
agent-toolkit card validate my-card.json

# 启动通信桥接
agent-toolkit bridge start
```

## 📦 核心功能

### 1. Agent扫描与发现
- 跨平台进程扫描
- MCP服务器检测
- 实时状态监控
- 告警通知

### 2. Agent Card管理
- 可视化编辑器
- JSON Schema验证
- 模板库
- 版本控制

### 3. 通信桥接
- 多协议支持（MCP、A2A、HTTP、WebSocket）
- 统一消息格式
- 负载均衡
- 服务发现

### 4. 监控与日志
- 性能指标收集
- 错误日志分析
- 趋势可视化
- 告警规则引擎

## 🛠️ 开发指南

### 贡献新语言实现

我们欢迎用任何语言实现核心功能：

1. 克隆仓库
2. 在 `cli/` 下创建新语言目录
3. 实现核心接口
4. 添加测试
5. 提交PR

### 核心接口

```go
// Go接口定义
type Scanner interface {
    Scan() ([]Agent, error)
    Watch(ctx context.Context) (<-chan AgentEvent, error)
}

type Validator interface {
    Validate(card *AgentCard) (*ValidationResult, error)
    ValidateFile(path string) (*ValidationResult, error)
}
```

## 📚 文档

- [架构设计](docs/architecture.md)
- [API参考](docs/api.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## 📄 许可证

MIT License
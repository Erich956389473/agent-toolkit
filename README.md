[English](./README_EN.md) | 中文

---

# Agent Toolkit

> 统一的 CLI 工具包 — 管理 Agent 清单、卡片、验证和桥接

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Erich956389473/agent-toolkit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 功能特性

- **统一入口** — 一个工具管理所有 Agent 功能
- **清单管理** — 扫描和管理 Agent 清单
- **卡片编辑** — 创建和编辑 Agent Card
- **验证功能** — 验证 Agent Card 规范
- **桥接服务** — Agent 间通信桥梁

## 🚀 快速开始

### 安装

`ash
# Go 版本
go install github.com/Erich956389473/agent-toolkit/cli/go@latest

# Python 版本
pip install agent-toolkit
`

### 使用

`ash
# 查看帮助
agent-toolkit --help

# 扫描 Agent
agent-toolkit scan

# 验证卡片
agent-toolkit validate card.json

# 启动桥接
agent-toolkit bridge start
`

## 📖 工具集

| 工具 | 说明 | 语言 |
|------|------|------|
| scan | 扫描本地 Agent | Go |
| alidate | 验证 Agent Card | Go |
| ridge | Agent 桥接服务 | Go |
| edit | 卡片编辑器 | Python |

## 🛠️ 开发

`ash
# Go 构建
cd cli/go && go build

# Python 安装
cd cli/python && pip install -e .
`

## 📦 技术栈

- **语言:** Go, Python
- **CLI:** Cobra (Go), Click (Python)
- **License:** MIT

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

**Author:** Erich Lee | [GitHub](https://github.com/Erich956389473)

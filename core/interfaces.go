package core

import (
	"context"
	"time"
)

// Agent 表示一个AI Agent
type Agent struct {
	ID          string            `json:"id"`
	Name        string            `json:"name"`
	Type        string            `json:"type"`
	Status      string            `json:"status"`
	PID         int               `json:"pid"`
	CommandLine string            `json:"command_line"`
	StartedAt   time.Time         `json:"started_at"`
	Metadata    map[string]string `json:"metadata"`
}

// AgentCard 表示A2A Agent Card
type AgentCard struct {
	Name               string       `json:"name"`
	Description        string       `json:"description"`
	URL                string       `json:"url"`
	Version            string       `json:"version"`
	IconURL            string       `json:"icon_url,omitempty"`
	Provider           *Provider    `json:"provider,omitempty"`
	Capabilities       []string     `json:"capabilities,omitempty"`
	DefaultInputModes  []string     `json:"default_input_modes,omitempty"`
	DefaultOutputModes []string     `json:"default_output_modes,omitempty"`
	Skills             []Skill      `json:"skills,omitempty"`
}

// Provider 表示Agent提供者信息
type Provider struct {
	Organization string `json:"organization,omitempty"`
	URL          string `json:"url,omitempty"`
}

// Skill 表示Agent技能
type Skill struct {
	ID          string   `json:"id"`
	Name        string   `json:"name"`
	Description string   `json:"description,omitempty"`
	Examples    []string `json:"examples,omitempty"`
}

// ValidationResult 验证结果
type ValidationResult struct {
	Valid    bool     `json:"valid"`
	Errors   []string `json:"errors,omitempty"`
	Warnings []string `json:"warnings,omitempty"`
}

// Message 表示Agent间消息
type Message struct {
	From      string            `json:"from"`
	To        string            `json:"to"`
	Content   interface{}       `json:"content"`
	Metadata  map[string]string `json:"metadata,omitempty"`
	Timestamp time.Time         `json:"timestamp"`
}

// Scanner 扫描器接口
type Scanner interface {
	// Scan 扫描所有本地Agent
	Scan() ([]Agent, error)
	// Watch 监控Agent变化
	Watch(ctx context.Context) (<-chan AgentEvent, error)
}

// AgentEvent Agent事件
type AgentEvent struct {
	Type  string `json:"type"` // "add", "remove", "update"
	Agent Agent  `json:"agent"`
}

// Editor 编辑器接口
type Editor interface {
	// Create 创建新的Agent Card
	Create(card *AgentCard) error
	// Update 更新Agent Card
	Update(card *AgentCard) error
	// Delete 删除Agent Card
	Delete(id string) error
	// Get 获取Agent Card
	Get(id string) (*AgentCard, error)
	// List 列出所有Agent Card
	List() ([]*AgentCard, error)
}

// Validator 验证器接口
type Validator interface {
	// Validate 验证Agent Card
	Validate(card *AgentCard) (*ValidationResult, error)
	// ValidateFile 验证Agent Card文件
	ValidateFile(path string) (*ValidationResult, error)
	// ValidateJSON 验证JSON字符串
	ValidateJSON(jsonStr string) (*ValidationResult, error)
}

// Bridge 桥接器接口
type Bridge interface {
	// RegisterAdapter 注册协议适配器
	RegisterAdapter(protocol string, adapter Adapter) error
	// Send 发送消息
	Send(message *Message) error
	// Receive 接收消息
	Receive(ctx context.Context) (<-chan *Message, error)
	// GetSupportedProtocols 获取支持的协议
	GetSupportedProtocols() []string
}

// Adapter 协议适配器接口
type Adapter interface {
	// Connect 连接到协议端点
	Connect(endpoint string) error
	// Disconnect 断开连接
	Disconnect() error
	// Send 发送消息
	Send(message *Message) error
	// Receive 接收消息
	Receive(ctx context.Context) (<-chan *Message, error)
	// GetProtocol 获取协议名称
	GetProtocol() string
}
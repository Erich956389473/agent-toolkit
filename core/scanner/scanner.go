package scanner

import (
	"context"
	"sync"
	"time"

	"github.com/agent-toolkit/core"
)

// Scanner 实现了core.Scanner接口
type Scanner struct {
	agents map[string]core.Agent
	mu     sync.RWMutex
}

// NewScanner 创建一个新的Scanner实例
func NewScanner() *Scanner {
	return &Scanner{
		agents: make(map[string]core.Agent),
	}
}

// Scan 扫描所有本地Agent
func (s *Scanner) Scan() ([]core.Agent, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	agents := make([]core.Agent, 0, len(s.agents))
	for _, agent := range s.agents {
		agents = append(agents, agent)
	}
	return agents, nil
}

// Watch 监控Agent变化
func (s *Scanner) Watch(ctx context.Context) (<-chan core.AgentEvent, error) {
	ch := make(chan core.AgentEvent)

	go func() {
		defer close(ch)
		ticker := time.NewTicker(1 * time.Second)
		defer ticker.Stop()

		for {
			select {
			case <-ctx.Done():
				return
			case <-ticker.C:
				// 模拟扫描变化
				s.mu.RLock()
				agentCount := len(s.agents)
				s.mu.RUnlock()

				if agentCount == 0 {
					// 模拟添加一个Agent
					agent := core.Agent{
						ID:          "mock-agent-1",
						Name:        "Mock Agent",
						Type:        "mock",
						Status:      "running",
						PID:         12345,
						CommandLine: "mock-agent --config config.yaml",
						StartedAt:   time.Now(),
						Metadata:    map[string]string{"version": "1.0.0"},
					}

					s.mu.Lock()
					s.agents[agent.ID] = agent
					s.mu.Unlock()

					select {
					case ch <- core.AgentEvent{
						Type:  "add",
						Agent: agent,
					}:
					case <-ctx.Done():
						return
					}
				}
			}
		}
	}()

	return ch, nil
}

// AddAgent 添加一个Agent（用于测试和模拟）
func (s *Scanner) AddAgent(agent core.Agent) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.agents[agent.ID] = agent
}

// RemoveAgent 移除一个Agent
func (s *Scanner) RemoveAgent(id string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.agents, id)
}

// GetAgent 获取一个Agent
func (s *Scanner) GetAgent(id string) (core.Agent, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	agent, ok := s.agents[id]
	return agent, ok
}
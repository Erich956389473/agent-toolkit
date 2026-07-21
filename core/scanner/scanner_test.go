package scanner

import (
	"context"
	"testing"
	"time"

	"github.com/agent-toolkit/core"
)

func TestNewScanner(t *testing.T) {
	s := NewScanner()
	if s == nil {
		t.Fatal("NewScanner() returned nil")
	}
}

func TestScanner_Scan(t *testing.T) {
	s := NewScanner()
	agents, err := s.Scan()
	if err != nil {
		t.Fatalf("Scan() error: %v", err)
	}

	// 扫描结果应该是空的，因为没有运行的Agent
	if len(agents) != 0 {
		t.Errorf("Scan() returned %d agents, want 0", len(agents))
	}
}

func TestScanner_Watch(t *testing.T) {
	s := NewScanner()
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	events, err := s.Watch(ctx)
	if err != nil {
		t.Fatalf("Watch() error: %v", err)
	}

	// 应该没有事件
	select {
	case event := <-events:
		t.Errorf("Watch() received event: %v", event)
	case <-ctx.Done():
		// 正常超时
	}
}

func TestScanner_ScanWithMock(t *testing.T) {
	// 创建一个模拟的Scanner
	mock := &MockScanner{
		agents: []core.Agent{
			{
				ID:     "test-agent-1",
				Name:   "Test Agent",
				Type:   "test",
				Status: "running",
				PID:    12345,
			},
		},
	}

	agents, err := mock.Scan()
	if err != nil {
		t.Fatalf("Mock Scan() error: %v", err)
	}

	if len(agents) != 1 {
		t.Fatalf("Mock Scan() returned %d agents, want 1", len(agents))
	}

	if agents[0].ID != "test-agent-1" {
		t.Errorf("Agent ID = %s, want test-agent-1", agents[0].ID)
	}
}

// MockScanner 是一个模拟的Scanner实现
type MockScanner struct {
	agents []core.Agent
}

func (m *MockScanner) Scan() ([]core.Agent, error) {
	return m.agents, nil
}

func (m *MockScanner) Watch(ctx context.Context) (<-chan core.AgentEvent, error) {
	ch := make(chan core.AgentEvent)
	go func() {
		defer close(ch)
		<-ctx.Done()
	}()
	return ch, nil
}
import { DashboardData, ConsciousnessState, RealityStatus, Task, ApprovalRequest, Communication, Transaction, KPI, BusinessWorkflow, ConsciousnessHistory, RealityScenario, TemporalTask } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchConsciousnessState(entityId: string = "system_core"): Promise<ConsciousnessState> {
  const response = await fetch(`${API_BASE_URL}/consciousness/state?entity_id=${entityId}`);
  if (!response.ok) throw new Error("Failed to fetch consciousness state");
  const data = await response.json();
  return data.consciousness_state;
}

export async function fetchRealityStatus(domain: string = "primary"): Promise<RealityStatus> {
  const response = await fetch(`${API_BASE_URL}/reality/consistency?domain=${domain}`);
  if (!response.ok) throw new Error("Failed to fetch reality status");
  const data = await response.json();
  return data.consistency_report;
}

export async function fetchDashboardData(): Promise<DashboardData> {
  // In a real scenario, this might be a single endpoint or parallel fetches
  // For now, we'll simulate the rollup or fetch what we can
  try {
    const consciousness = await fetchConsciousnessState();
    const reality = await fetchRealityStatus();
    
    // Placeholder for tasks/health until endpoints are confirmed
    return {
      consciousness,
      reality,
      tasks: {
        pending_count: 3,
        completed_today: 14,
        active_chains: 5
      },
      health: {
        status: "healthy",
        uptime: "14d 6h 22m",
        version: "Diamond v2.0"
      }
    };
  } catch (error) {
    console.error("Dashboard data fetch error:", error);
    throw error;
  }
}

export async function fetchTasks(): Promise<Task[]> {
  // Simulating fetching tasks from /Needs_Action via backend
  // In reality, would be: const response = await fetch(`${API_BASE_URL}/tasks/pending`);
  return [
    {
      id: "EMAIL_123",
      type: "email",
      from: "investor@example.com",
      priority: "high",
      status: "pending",
      created: new Date().toISOString(),
      subject: "Investment Opportunity",
      content: "I'm interested in the new Diamond Tier rollout. Can we discuss?",
      suggested_actions: ["Draft reply", "Schedule meeting", "Archive"]
    },
    {
      id: "WA_456",
      type: "whatsapp",
      from: "+1234567890",
      priority: "critical",
      status: "pending",
      created: new Date(Date.now() - 3600000).toISOString(),
      content: "Urgent: Payment gateway is down in simulation scenario #4.",
      suggested_actions: ["Check logs", "Restart service", "Alert engineering"]
    }
  ] as Task[];
}
export async function fetchApprovals(): Promise<ApprovalRequest[]> {
  return [
    {
      id: "APP_789",
      type: "approval_request",
      action: "send_email",
      recipient: "investor@example.com",
      reason: "Proposed reply to investment inquiry",
      created: new Date().toISOString(),
      expires: new Date(Date.now() + 86400000).toISOString(),
      status: "pending",
      details: "Subject: RE: Investment Opportunity\n\nDear Investor, we would be happy to discuss..."
    }
  ] as ApprovalRequest[];
}

export async function fetchCommunications(): Promise<Communication[]> {
  return [
    {
      id: "COM_1",
      platform: "email",
      contact_name: "John Doe",
      contact_identifier: "john@example.com",
      last_message: "The proposal looks solid. Let's move forward.",
      last_timestamp: new Date().toISOString(),
      unread_count: 0,
      sentiment_score: 0.85,
      status: "active",
      history: [
        { id: "M1", sender: "John Doe", content: "Hey ELYX, looking for the proposal.", timestamp: "2026-02-04T10:00:00Z", is_ai: false },
        { id: "M2", sender: "ELYX", content: "Generating proposal now. One moment.", timestamp: "2026-02-04T10:01:00Z", is_ai: true },
        { id: "M3", sender: "John Doe", content: "The proposal looks solid. Let's move forward.", timestamp: "2026-02-04T13:00:00Z", is_ai: false }
      ]
    },
    {
      id: "COM_2",
      platform: "whatsapp",
      contact_name: "Sarah Smith",
      contact_identifier: "+1234567890",
      last_message: "Can you check the latest reality leak on domain #4?",
      last_timestamp: new Date(Date.now() - 10 * 60000).toISOString(),
      unread_count: 1,
      sentiment_score: 0.45,
      status: "needs_reply",
      history: [
        { id: "M4", sender: "Sarah Smith", content: "Can you check the latest reality leak on domain #4?", timestamp: "2026-02-04T13:30:00Z", is_ai: false }
      ]
    }
  ] as Communication[];
}

export async function fetchTransactions(): Promise<Transaction[]> {
  return [
    { id: "T1", type: "income", amount: 4500.00, category: "Services", merchant: "Client A", date: new Date().toISOString(), status: "completed" },
    { id: "T2", type: "expense", amount: 120.50, category: "Software", merchant: "Vercel", date: new Date(Date.now() - 86400000).toISOString(), status: "completed" },
    { id: "T3", type: "expense", amount: 2500.00, category: "Infrastructure", merchant: "AWS", date: new Date(Date.now() - 172800000).toISOString(), status: "pending" }
  ] as Transaction[];
}

export async function fetchKPIs(): Promise<KPI[]> {
  return [
    { label: "Monthly Revenue", value: "$45,210", change: 12.5, trend: "up" },
    { label: "Operating Efficiency", value: "94.2%", change: -2.1, trend: "down" },
    { label: "New Leads", value: "142", change: 8.4, trend: "up" },
    { label: "Churn Rate", value: "0.8%", change: 0, trend: "neutral" }
  ] as KPI[];
}

export async function fetchWorkflows(): Promise<BusinessWorkflow[]> {
  return [
    { id: "WF1", name: "Weekly Financial Reconciliation", status: "active", efficiency: 98, steps_completed: 4, total_steps: 5, last_run: new Date().toISOString() },
    { id: "WF2", name: "Client Onboarding Simulation", status: "completed", efficiency: 100, steps_completed: 12, total_steps: 12, last_run: new Date(Date.now() - 3600000).toISOString() },
    { id: "WF3", name: "Social Media Sentiment Loop", status: "paused", efficiency: 82, steps_completed: 1, total_steps: 3, last_run: new Date(Date.now() - 7200000).toISOString() }
  ] as BusinessWorkflow[];
}

export async function fetchConsciousnessHistory(): Promise<ConsciousnessHistory[]> {
  // Generate mock history data for the last 24 hours
  return Array.from({ length: 24 }, (_, i) => ({
    timestamp: new Date(Date.now() - (23 - i) * 3600000).toISOString(),
    phi: 85 + Math.random() * 10,
    self_awareness: 0.8 + Math.random() * 0.15,
    attention: 0.7 + Math.random() * 0.25
  })) as ConsciousnessHistory[];
}

export async function fetchRealityScenarios(): Promise<RealityScenario[]> {
  return [
    { 
      id: "S1", 
      name: "Global Market Expansion", 
      type: "strategic", 
      probability: 0.65, 
      status: "simulating", 
      impact_score: 92, 
      causal_links: 1422,
      description: "Analyzing the impact of entering the EU market with a focus on local compliance.",
      last_calculation: new Date().toISOString() 
    },
    { 
      id: "S2", 
      name: "Competitor Hostile Takeover", 
      type: "business", 
      probability: 0.12, 
      status: "diverged", 
      impact_score: 45, 
      causal_links: 890,
      description: "Low probability event with extreme volatility in primary revenue streams.",
      last_calculation: new Date(Date.now() - 7200000).toISOString() 
    },
    { 
      id: "S3", 
      name: "Diamond Tier Customer Churn", 
      type: "financial", 
      probability: 0.05, 
      status: "stable", 
      impact_score: 98, 
      causal_links: 2105,
      description: "Scenario where top 5% of users exit simultaneously. Worst case projection.",
      last_calculation: new Date(Date.now() - 3600000).toISOString() 
    },
    { 
      id: "S4", 
      name: "Standard Growth Path", 
      type: "strategic", 
      probability: 0.88, 
      status: "anchored", 
      impact_score: 15, 
      causal_links: 450,
      description: "Baseline projection with minimal risk and organic growth parameters.",
      last_calculation: new Date().toISOString() 
    }
  ] as RealityScenario[];
}

export async function fetchTemporalTasks(): Promise<TemporalTask[]> {
  return [
    { 
      id: "TT1", 
      title: "Quarterly Financial Prophet Sync", 
      scheduled_time: new Date(Date.now() + 3600000).toISOString(), 
      timeline: "primary", 
      priority: "high", 
      status: "scheduled", 
      impact_coefficient: 0.88 
    },
    { 
      id: "TT2", 
      title: "Historical Data Reconciliation", 
      scheduled_time: new Date(Date.now() - 7200000).toISOString(), 
      timeline: "historical", 
      priority: "medium", 
      status: "completed", 
      impact_coefficient: 0.42 
    },
    { 
      id: "TT3", 
      title: "Simulated Market Crash Analysis", 
      scheduled_time: new Date().toISOString(), 
      timeline: "simulated", 
      priority: "high", 
      status: "running", 
      impact_coefficient: 0.95 
    },
    { 
      id: "TT4", 
      title: "Next-Year Revenue Projection", 
      scheduled_time: new Date(Date.now() + 86400000).toISOString(), 
      timeline: "simulated", 
      priority: "low", 
      status: "scheduled", 
      impact_coefficient: 0.65 
    }
  ] as TemporalTask[];
}

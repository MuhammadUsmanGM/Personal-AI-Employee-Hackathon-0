import { DashboardData, ConsciousnessState, RealityStatus, Task, ApprovalRequest } from "./types";

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

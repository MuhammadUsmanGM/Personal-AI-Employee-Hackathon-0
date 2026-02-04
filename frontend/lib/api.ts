import { DashboardData, ConsciousnessState, RealityStatus } from "./types";

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

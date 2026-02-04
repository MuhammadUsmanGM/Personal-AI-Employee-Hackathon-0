export interface ConsciousnessState {
  id: string;
  entity_id: string;
  entity_type: string;
  state_type: string;
  attention_focus: Record<string, any>;
  self_awareness_level: number;
  introspection_depth: number;
  emotional_state: Record<string, any>;
  cognitive_load: number;
  creativity_level: number;
  memory_integration_status: string;
  attention_coherence: number;
  self_model_accuracy: number;
  phi: number;
  updated_at: string;
}

export interface RealityStatus {
  domain: string;
  current_score: number;
  stability_index: number;
  anchoring_strength: number;
  boundary_integrity: number;
  current_status: string;
  next_check_due: string;
}

export interface TaskStatus {
  pending_count: number;
  completed_today: number;
  active_chains: number;
}

export interface DashboardData {
  consciousness: ConsciousnessState;
  reality: RealityStatus;
  tasks: TaskStatus;
  health: {
    status: string;
    uptime: string;
    version: string;
  };
}

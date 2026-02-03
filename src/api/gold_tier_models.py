"""
Gold Tier API Models for Personal AI Employee System
Additional models for advanced AI capabilities, enterprise features, and strategic planning
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class StrategicObjectiveStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    DELAYED = "delayed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class StrategicObjectivePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    STRATEGIC = "strategic"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    REPUTATIONAL = "reputational"


class ComplianceStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    EXEMPT = "exempt"
    PENDING_REVIEW = "pending_review"


class ResourceAllocationStatus(str, Enum):
    PLANNED = "planned"
    ALLOCATED = "allocated"
    IN_USE = "in_use"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ResourceAllocationRequest(BaseModel):
    """Request model for resource allocation"""
    resource_type: str = Field(..., description="Type of resource (human, financial, technical, time, computational)")
    resource_name: str = Field(..., description="Name of the resource")
    allocated_to_entity: str = Field(..., description="ID of entity resource is allocated to")
    allocated_to_type: str = Field(..., description="Type of entity (task, project, objective, process)")
    quantity: float = Field(..., description="Quantity of resource to allocate")
    unit: str = Field(..., description="Unit of measurement (hours, dollars, units, etc.)")
    allocation_period_start: datetime = Field(..., description="Start of allocation period")
    allocation_period_end: datetime = Field(..., description="End of allocation period")
    budget_code: Optional[str] = Field(None, description="Budget code for allocation")
    allocated_by: str = Field(..., description="User who allocated the resource")
    approved_by: Optional[str] = Field(None, description="User who approved the allocation")
    priority: Optional[str] = Field("medium", description="Priority of allocation")
    description: Optional[str] = Field(None, description="Description of the allocation")


class ResourceAllocationResponse(BaseModel):
    """Response model for resource allocation"""
    id: str
    resource_type: str
    resource_name: str
    allocated_to_entity: str
    allocated_to_type: str
    quantity: float
    unit: str
    allocation_period_start: datetime
    allocation_period_end: datetime
    budget_code: Optional[str]
    allocated_by: str
    approved_by: Optional[str]
    status: ResourceAllocationStatus
    priority: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    description: Optional[str]


class StrategicObjectiveRequest(BaseModel):
    """Request model for strategic objective creation"""
    title: str = Field(..., max_length=255, description="Title of the strategic objective")
    description: Optional[str] = Field(None, description="Detailed description of the objective")
    organization_id: str = Field(..., description="Organization ID")
    owner_id: str = Field(..., description="User ID of the owner")
    priority: StrategicObjectivePriority = Field(StrategicObjectivePriority.MEDIUM, description="Priority of the objective")
    start_date: datetime = Field(..., description="Start date of the objective")
    target_date: datetime = Field(..., description="Target completion date")
    business_value: Optional[float] = Field(None, description="Estimated business value")
    cost_estimate: Optional[float] = Field(None, description="Estimated cost")
    key_results: Optional[Dict[str, Any]] = Field(None, description="Key results for objective tracking")
    dependencies: Optional[Dict[str, Any]] = Field(None, description="Dependencies on other objectives")
    success_metrics: Optional[Dict[str, Any]] = Field(None, description="Metrics to measure success")


class StrategicObjectiveResponse(BaseModel):
    """Response model for strategic objective"""
    id: str
    title: str
    description: Optional[str]
    organization_id: str
    owner_id: str
    priority: StrategicObjectivePriority
    status: StrategicObjectiveStatus
    start_date: datetime
    target_date: datetime
    completion_date: Optional[datetime]
    progress_percentage: Optional[float]
    business_value: Optional[float]
    cost_estimate: Optional[float]
    current_cost: Optional[float]
    key_results: Optional[Dict[str, Any]]
    dependencies: Optional[Dict[str, Any]]
    success_metrics: Optional[Dict[str, Any]]
    risk_factors: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    ai_analysis: Optional[Dict[str, Any]]


class RiskAssessmentRequest(BaseModel):
    """Request model for risk assessment"""
    entity_id: str = Field(..., description="ID of the entity being assessed")
    entity_type: str = Field(..., description="Type of entity (task, objective, process, system, project)")
    risk_category: RiskCategory = Field(..., description="Category of the risk")
    risk_description: str = Field(..., description="Description of the risk")
    probability: float = Field(..., ge=0.0, le=1.0, description="Probability of the risk occurring (0-1)")
    impact: float = Field(..., ge=0.0, le=1.0, description="Impact of the risk if it occurs (0-1)")
    owner_id: str = Field(..., description="User ID of the risk owner")
    mitigation_strategy: Optional[str] = Field(None, description="Strategy for mitigating the risk")
    timeline: Optional[Dict[str, Any]] = Field(None, description="Timeline for mitigation")


class RiskAssessmentResponse(BaseModel):
    """Response model for risk assessment"""
    id: str
    entity_id: str
    entity_type: str
    risk_category: RiskCategory
    risk_description: str
    probability: float
    impact: float
    risk_score: float
    risk_level: RiskLevel
    mitigation_strategy: Optional[str]
    owner_id: str
    status: str  # Could define as enum if needed
    mitigation_efforts: Optional[Dict[str, Any]]
    timeline: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    ai_generated: bool
    ai_confidence: Optional[float]


class ComplianceRecordRequest(BaseModel):
    """Request model for compliance record"""
    regulation_id: str = Field(..., description="ID of the regulation/compliance requirement")
    regulation_name: str = Field(..., description="Name of the regulation")
    jurisdiction: str = Field(..., description="Jurisdiction of the regulation")
    requirement_description: str = Field(..., description="Description of the requirement")
    entity_affected: str = Field(..., description="Which entity the requirement affects")
    entity_type: str = Field(..., description="Type of entity (task, process, system, document, activity)")
    responsible_party: str = Field(..., description="Party responsible for compliance")
    evidence_documents: Optional[Dict[str, Any]] = Field(None, description="References to evidence of compliance")
    review_schedule: Optional[Dict[str, Any]] = Field(None, description="Schedule for compliance reviews")


class ComplianceRecordResponse(BaseModel):
    """Response model for compliance record"""
    id: str
    regulation_id: str
    regulation_name: str
    jurisdiction: str
    requirement_description: str
    entity_affected: str
    entity_type: str
    compliance_status: ComplianceStatus
    evidence_documents: Optional[Dict[str, Any]]
    review_schedule: Optional[Dict[str, Any]]
    last_review_date: Optional[datetime]
    next_review_date: Optional[datetime]
    responsible_party: str
    compliance_notes: Optional[str]
    audit_trail: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    ai_compliance_check: Optional[Dict[str, Any]]
    automated_monitoring: bool


class DecisionSupportRequest(BaseModel):
    """Request model for decision support"""
    problem_statement: str = Field(..., description="Clear statement of the problem to solve")
    options: List[Dict[str, Any]] = Field(..., description="List of possible options to evaluate")
    criteria_weights: Dict[str, float] = Field(..., description="Weights for different evaluation criteria")
    constraints: Optional[List[str]] = Field(None, description="Constraints that must be satisfied")
    timeframe: Optional[Dict[str, Any]] = Field(None, description="Timeframe considerations")


class DecisionSupportResponse(BaseModel):
    """Response model for decision support"""
    problem_statement: str
    recommended_option: Dict[str, Any]
    all_options_evaluated: List[Dict[str, Any]]
    confidence_score: float
    rationale: str
    risk_assessment: Dict[str, Any]
    implementation_steps: List[str]
    success_probability: float
    created_at: datetime


class BusinessIntelligenceReportRequest(BaseModel):
    """Request model for business intelligence report"""
    report_type: str = Field(..., description="Type of report (performance, trend, forecast, comparative, compliance, risk, strategic)")
    organization_id: str = Field(..., description="Organization ID")
    report_period_start: datetime = Field(..., description="Start of report period")
    report_period_end: datetime = Field(..., description="End of report period")
    key_metrics: Optional[List[str]] = Field(None, description="Specific metrics to include")
    visualizations: Optional[List[Dict[str, Any]]] = Field(None, description="Visualization configurations")
    recipients: Optional[List[str]] = Field(None, description="Recipients of the report")


class BusinessIntelligenceReportResponse(BaseModel):
    """Response model for business intelligence report"""
    id: str
    report_name: str
    report_type: str
    organization_id: str
    generated_by: str
    generated_at: datetime
    report_period_start: datetime
    report_period_end: datetime
    data_sources: Dict[str, Any]
    key_metrics: Dict[str, Any]
    insights: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    visualizations: Optional[Dict[str, Any]]
    recipients: Optional[List[str]]
    report_data: Dict[str, Any]
    ai_analysis_confidence: float
    report_format: str
    is_automated: bool


class PersonalizedDashboardRequest(BaseModel):
    """Request model for personalized dashboard"""
    user_id: str = Field(..., description="User ID for personalization")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    dashboard_type: str = Field("standard", description="Type of dashboard to generate")
    widget_preferences: Optional[Dict[str, Any]] = Field(None, description="Preferred widgets and layout")


class PersonalizedDashboardResponse(BaseModel):
    """Response model for personalized dashboard"""
    user_id: str
    organization_id: Optional[str]
    timestamp: datetime
    layout: Dict[str, Any]
    widgets: List[Dict[str, Any]]
    dynamic_content: Dict[str, Any]
    personalization_score: float
    last_updated: datetime


class AIInteractionRequest(BaseModel):
    """Request model for AI interaction"""
    user_input: str = Field(..., description="Input from the user")
    user_id: str = Field(..., description="User ID")
    context: Optional[Dict[str, Any]] = Field(None, description="Context for the interaction")
    interaction_mode: Optional[str] = Field("assistive", description="Mode of interaction (autonomous, assistive, collaborative, supervised)")


class AIInteractionResponse(BaseModel):
    """Response model for AI interaction"""
    response_text: str
    emotion_detected: str
    communication_style: str
    confidence: float
    suggested_next_actions: List[str]
    needs_clarification: bool
    ai_reasoning: Optional[Dict[str, Any]]
    processing_time_ms: float
    timestamp: datetime


class EnterpriseAnalyticsRequest(BaseModel):
    """Request model for enterprise analytics"""
    organization_id: str = Field(..., description="Organization ID")
    time_window_days: int = Field(30, description="Time window for analysis in days")
    include_strategic: bool = Field(True, description="Include strategic metrics")
    include_risk: bool = Field(True, description="Include risk metrics")
    include_compliance: bool = Field(True, description="Include compliance metrics")
    include_resources: bool = Field(True, description="Include resource metrics")


class EnterpriseAnalyticsResponse(BaseModel):
    """Response model for enterprise analytics"""
    organization_id: str
    timestamp: datetime
    time_window_days: int
    strategic_metrics: Dict[str, Any]
    risk_metrics: Dict[str, Any]
    compliance_metrics: Dict[str, Any]
    resource_metrics: Dict[str, Any]
    overall_health_score: float
    key_recommendations: List[str]
    trend_analysis: Dict[str, Any]
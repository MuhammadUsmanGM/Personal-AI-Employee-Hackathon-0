"""
Platinum Tier API Models for Personal AI Employee System
Additional models for quantum security, blockchain, IoT, AR/VR, and global operations
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class GlobalOperationStatus(str, Enum):
    PLANNED = "planned"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    GLOBAL_ESCALATION = "global_escalation"


class GlobalOperationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    GLOBAL_URGENT = "global_urgent"


class GlobalOperationRequest(BaseModel):
    """Request model for global operation creation"""
    operation_name: str = Field(..., max_length=255, description="Name of the global operation")
    description: Optional[str] = Field(None, description="Detailed description of the operation")
    organization_id: str = Field(..., description="Organization ID")
    owner_id: str = Field(..., description="User ID of the owner")
    priority: GlobalOperationPriority = Field(GlobalOperationPriority.MEDIUM, description="Priority of the operation")
    start_date: datetime = Field(..., description="Start date of the operation")
    end_date: datetime = Field(..., description="Target end date of the operation")
    regions_affected: List[str] = Field(..., description="List of regions affected by the operation")
    risk_assessment: Optional[Dict[str, Any]] = Field(None, description="Risk assessment for the operation")
    resource_allocation: Optional[Dict[str, Any]] = Field(None, description="Resource allocation for the operation")
    dependencies: Optional[Dict[str, Any]] = Field(None, description="Dependencies on other operations")
    success_metrics: Optional[Dict[str, Any]] = Field(None, description="Metrics to measure success")
    compliance_requirements: Optional[Dict[str, Any]] = Field(None, description="Compliance requirements")


class GlobalOperationUpdate(BaseModel):
    """Request model for global operation updates"""
    operation_name: Optional[str] = Field(None, max_length=255, description="Name of the global operation")
    description: Optional[str] = Field(None, description="Detailed description of the operation")
    status: Optional[GlobalOperationStatus] = Field(None, description="Status of the operation")
    priority: Optional[GlobalOperationPriority] = Field(None, description="Priority of the operation")
    end_date: Optional[datetime] = Field(None, description="Target end date of the operation")
    regions_affected: Optional[List[str]] = Field(None, description="List of regions affected by the operation")
    success_metrics: Optional[Dict[str, Any]] = Field(None, description="Metrics to measure success")


class GlobalOperationResponse(BaseModel):
    """Response model for global operation"""
    id: str
    operation_name: str
    description: Optional[str]
    organization_id: str
    owner_id: str
    status: GlobalOperationStatus
    priority: GlobalOperationPriority
    start_date: datetime
    end_date: datetime
    estimated_completion: Optional[datetime]
    actual_completion: Optional[datetime]
    regions_affected: List[str]
    global_impact_score: Optional[float]
    risk_assessment: Optional[Dict[str, Any]]
    resource_allocation: Optional[Dict[str, Any]]
    dependencies: Optional[Dict[str, Any]]
    success_metrics: Optional[Dict[str, Any]]
    blockchain_verification: Optional[Dict[str, Any]]
    quantum_security_measures: Optional[Dict[str, Any]]
    compliance_requirements: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    ai_analysis: Optional[Dict[str, Any]]
    federated_learning_contributions: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True


class PaginatedGlobalOperations(BaseModel):
    """Response model for paginated global operations"""
    operations: List[GlobalOperationResponse]
    pagination: Dict[str, Any]

    class Config:
        from_attributes = True


class QuantumKeyRequest(BaseModel):
    """Request model for quantum key creation"""
    key_type: str = Field("symmetric", description="Type of key (symmetric or asymmetric)")
    algorithm: str = Field("lattice-based", description="Quantum-safe algorithm to use")
    security_level: str = Field("quantum_safe", description="Security level (basic, enhanced, quantum_safe)")
    rotation_interval_hours: int = Field(24, description="Rotation interval in hours")


class QuantumKeyResponse(BaseModel):
    """Response model for quantum key"""
    id: str
    key_type: str
    algorithm: str
    security_level: str
    generation_date: str
    expiration_date: str
    rotation_interval_hours: int
    status: str
    next_rotation_date: str

    class Config:
        from_attributes = True


class QuantumEncryptRequest(BaseModel):
    """Request model for quantum encryption"""
    data: str = Field(..., description="Data to encrypt")
    key_id: Optional[str] = Field(None, description="ID of the key to use for encryption")
    algorithm: Optional[str] = Field(None, description="Algorithm to use for encryption")
    security_level: Optional[str] = Field("quantum_safe", description="Security level for encryption")


class QuantumEncryptResponse(BaseModel):
    """Response model for quantum encryption"""
    encrypted_data: str
    key_used: str
    algorithm_used: str
    encryption_date: str

    class Config:
        from_attributes = True


class QuantumDecryptRequest(BaseModel):
    """Request model for quantum decryption"""
    encrypted_data: str = Field(..., description="Data to decrypt")
    key_id: str = Field(..., description="ID of the key to use for decryption")
    nonce: Optional[str] = Field(None, description="Nonce for decryption")


class QuantumDecryptResponse(BaseModel):
    """Response model for quantum decryption"""
    decrypted_data: str
    decryption_date: str

    class Config:
        from_attributes = True


class QuantumTransactionType(str, Enum):
    PAYMENT = "payment"
    APPROVAL = "approval"
    DATA_EXCHANGE = "data_exchange"
    CONTRACT_EXECUTION = "contract_execution"
    IDENTITY_VERIFICATION = "identity_verification"
    SECURITY_AUDIT = "security_audit"


class QuantumTransactionRequest(BaseModel):
    """Request model for quantum transaction"""
    transaction_type: QuantumTransactionType = Field(..., description="Type of transaction")
    sender_id: str = Field(..., description="Sender ID")
    receiver_id: str = Field(..., description="Receiver ID")
    amount: Optional[float] = Field(None, description="Amount for payment transactions")
    currency: Optional[str] = Field("USD", description="Currency for payment transactions")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional transaction data")
    blockchain_network: str = Field("ethereum", description="Blockchain network to use")


class QuantumTransactionResponse(BaseModel):
    """Response model for quantum transaction"""
    transaction_id: str
    transaction_hash: str
    status: str
    estimated_gas: int

    class Config:
        from_attributes = True


class BlockchainEventType(str, Enum):
    SMART_CONTRACT_EXECUTION = "smart_contract_execution"
    TOKEN_TRANSFER = "token_transfer"
    IDENTITY_VERIFICATION = "identity_verification"
    DATA_PROOF = "data_proof"
    APPROVAL_RECORDING = "approval_recording"
    COMPLIANCE_LOGGING = "compliance_logging"


class BlockchainEventRequest(BaseModel):
    """Request model for blockchain event"""
    event_type: BlockchainEventType = Field(..., description="Type of blockchain event")
    blockchain_network: str = Field("ethereum", description="Blockchain network")
    contract_address: Optional[str] = Field(None, description="Smart contract address")
    event_data: Dict[str, Any] = Field(..., description="Event data")
    participants: List[str] = Field(..., description="Participants in the event")


class BlockchainEventResponse(BaseModel):
    """Response model for blockchain event"""
    id: str
    event_type: BlockchainEventType
    blockchain_network: str
    transaction_hash: str
    block_number: int
    contract_address: Optional[str]
    event_data: Dict[str, Any]
    participants: List[str]
    gas_consumed: int
    timestamp: datetime
    verification_status: str
    oracle_verifications: Optional[Dict[str, Any]]
    compliance_tags: Optional[List[str]]
    quantum_signature_verified: bool
    linked_tasks: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]
    ai_analysis: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class IoTDeviceType(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    GATEWAY = "gateway"
    EDGE_COMPUTER = "edge_computer"
    ROBOT = "robot"
    DRONE = "drone"
    SMART_HOME = "smart_home"
    INDUSTRIAL_AUTOMATION = "industrial_automation"


class IoTDeviceRequest(BaseModel):
    """Request model for IoT device registration"""
    device_name: str = Field(..., description="Name of the IoT device")
    device_type: IoTDeviceType = Field(..., description="Type of IoT device")
    manufacturer: str = Field(..., description="Device manufacturer")
    model: str = Field(..., description="Device model")
    serial_number: str = Field(..., description="Serial number of the device")
    mac_address: Optional[str] = Field(None, description="MAC address of the device")
    ip_address: Optional[str] = Field(None, description="IP address of the device")
    location_coordinates: Optional[Dict[str, float]] = Field(None, description="Geographic coordinates")
    region: Optional[str] = Field(None, description="Region where device is deployed")
    security_level: str = Field("enhanced", description="Security level (basic, enhanced, quantum_secure)")
    capabilities: Optional[Dict[str, Any]] = Field(None, description="Device capabilities")
    compliance_certifications: Optional[List[str]] = Field(None, description="Compliance certifications")


class IoTDeviceResponse(BaseModel):
    """Response model for IoT device"""
    id: str
    device_name: str
    device_type: IoTDeviceType
    manufacturer: str
    model: str
    serial_number: str
    mac_address: Optional[str]
    ip_address: Optional[str]
    firmware_version: Optional[str]
    last_seen: Optional[datetime]
    status: str
    location_coordinates: Optional[Dict[str, float]]
    region: Optional[str]
    security_level: str
    last_quantum_key_rotation: Optional[datetime]
    supported_protocols: Optional[List[str]]
    capabilities: Optional[Dict[str, Any]]
    sensor_data_schema: Optional[Dict[str, Any]]
    actuator_commands: Optional[Dict[str, Any]]
    blockchain_identity: Optional[str]
    compliance_certifications: Optional[List[str]]
    maintenance_schedule: Optional[Dict[str, Any]]
    linked_users: Optional[List[str]]
    ai_behavior_model: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    last_quantum_verification: Optional[datetime]

    class Config:
        from_attributes = True


class ARVRInterfaceType(str, Enum):
    AR_OVERLAY = "ar_overlay"
    VR_ENVIRONMENT = "vr_environment"
    MIXED_REALITY = "mixed_reality"
    HOLOGRAPHIC = "holographic"
    IMMERSIVE_DASHBOARD = "immersive_dashboard"
    SPATIAL_ANALYTICS = "spatial_analytics"


class ARVRInterfaceRequest(BaseModel):
    """Request model for AR/VR interface creation"""
    interface_name: str = Field(..., description="Name of the AR/VR interface")
    interface_type: ARVRInterfaceType = Field(..., description="Type of AR/VR interface")
    description: Optional[str] = Field(None, description="Description of the interface")
    visibility: str = Field("private", description="Visibility (private, shared, public, enterprise, quantum_secure)")
    supported_platforms: List[str] = Field(["windows"], description="Supported platforms")
    spatial_coordinates: Optional[Dict[str, float]] = Field(None, description="Spatial coordinates in virtual space")
    complexity_level: str = Field("basic", description="Complexity level (basic, intermediate, advanced, quantum_enhanced)")
    ai_assistant_integration: Optional[Dict[str, Any]] = Field(None, description="AI assistant configuration")
    blockchain_verification_required: bool = Field(False, description="Whether blockchain verification is required")
    quantum_secure_rendering: bool = Field(False, description="Whether rendering is quantum secure")
    resource_requirements: Optional[Dict[str, Any]] = Field(None, description="Computational requirements")


class ARVRInterfaceResponse(BaseModel):
    """Response model for AR/VR interface"""
    id: str
    interface_name: str
    interface_type: ARVRInterfaceType
    description: Optional[str]
    creator_id: Optional[str]
    visibility: str
    supported_platforms: List[str]
    spatial_coordinates: Optional[Dict[str, float]]
    permissions: Optional[Dict[str, Any]]
    complexity_level: str
    ai_assistant_integration: Optional[Dict[str, Any]]
    blockchain_verification_required: bool
    quantum_secure_rendering: bool
    resource_requirements: Optional[Dict[str, Any]]
    interactivity_level: str
    data_visualization_configs: Optional[Dict[str, Any]]
    collaboration_features: Optional[Dict[str, Any]]
    ai_behavior_scripts: Optional[Dict[str, Any]]
    security_clearance_level: str
    compliance_requirements: Optional[Dict[str, Any]]
    user_interaction_tracking: Optional[Dict[str, Any]]
    performance_metrics: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    last_quantum_security_check: Optional[datetime]

    class Config:
        from_attributes = True
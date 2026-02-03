"""
Database models and initialization for Silver Tier Personal AI Employee System
Extends Bronze Tier functionality with enhanced data models for analytics and learning
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid
from typing import Optional

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Task(Base):
    """
    Enhanced Task model extending Bronze Tier functionality
    """
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='pending')  # pending, processing, completed, failed, awaiting_approval
    priority = Column(String(20), default='medium')  # low, medium, high, critical
    category = Column(String(50), default='custom')  # email, file, calendar, crm, custom
    source = Column(String(50), default='api')  # gmail, whatsapp, filesystem, calendar, api
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime)
    assigned_to = Column(String(255))
    completed_at = Column(DateTime)
    task_metadata = Column(JSON)  # source-specific data
    parent_task_id = Column(String, ForeignKey('tasks.id'))  # for hierarchical tasks
    estimated_duration = Column(Integer)  # minutes
    actual_duration = Column(Integer)  # minutes
    confidence_score = Column(Float)  # 0-1 AI's confidence in completion
    retry_count = Column(Integer, default=0)
    last_error = Column(Text)

    # Relationships
    children = relationship("Task", back_populates="parent")
    parent = relationship("Task", remote_side=[id], back_populates="children")
    approval_request = relationship("ApprovalRequest", uselist=False, back_populates="task")

class ApprovalRequest(Base):
    """
    Enhanced ApprovalRequest model extending Bronze Tier functionality
    """
    __tablename__ = 'approval_requests'

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey('tasks.id'), nullable=False)
    requester = Column(String(255))  # email or system
    approver = Column(String(255))  # email or system
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    status = Column(String(20), default='pending')  # pending, approved, rejected, expired
    approval_level = Column(String(20))  # manager, director, executive
    business_impact = Column(String(20))  # low, medium, high, critical
    financial_impact_amount = Column(Float)
    financial_impact_currency = Column(String(10))
    escalation_required = Column(Boolean, default=False)
    escalation_reason = Column(Text)
    approved_by = Column(String(255))
    approved_at = Column(DateTime)
    rejected_by = Column(String(255))
    rejected_at = Column(DateTime)

    # Relationship
    task = relationship("Task", back_populates="approval_request")

class UserPreference(Base):
    """
    User Preference model for learning and adaptation
    """
    __tablename__ = 'user_preferences'

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String(255), nullable=False)  # email or identifier
    preference_key = Column(String(255), nullable=False)  # email_response_style, approval_threshold, etc.
    preference_value = Column(Text)  # JSON serialized for complex values
    preference_type = Column(String(20))  # behavioral, operational, security, communication
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confidence_level = Column(Float)  # 0-1, how certain the system is about this preference
    usage_count = Column(Integer, default=0)  # how many times this preference has been applied
    effectiveness_score = Column(Float)  # -1 to 1, positive if good, negative if bad

class InteractionLog(Base):
    """
    Interaction Log model for tracking all interactions for learning
    """
    __tablename__ = 'interaction_logs'

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String(255), nullable=False)  # email or identifier
    interaction_type = Column(String(20))  # approval, correction, feedback, override, query
    task_id = Column(String, ForeignKey('tasks.id'))  # optional, foreign key to Task
    action_taken = Column(Text)  # description of user action
    system_response = Column(Text)  # description of system behavior
    timestamp = Column(DateTime, default=datetime.utcnow)
    context_snapshot = Column(JSON)  # system state at time of interaction
    outcome = Column(String(10))  # positive, negative, neutral
    feedback_text = Column(Text)  # optional, user feedback
    learning_applied = Column(Boolean, default=False)  # whether this influenced future behavior

    # Relationship
    task = relationship("Task")

class AnalyticsSnapshot(Base):
    """
    Analytics Snapshot model for performance and usage analytics
    """
    __tablename__ = 'analytics_snapshots'

    id = Column(String, primary_key=True, default=generate_uuid)
    snapshot_time = Column(DateTime, default=datetime.utcnow)
    metric_name = Column(String(100), nullable=False)  # tasks_processed, approval_rate, response_time
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20))  # count, percentage, seconds, bytes
    dimension_labels = Column(JSON)  # tags like {"category": "email", "priority": "high"}
    calculated_from = Column(String(255))  # source of calculation

class IntegrationConnection(Base):
    """
    Integration Connection model for external service connections
    """
    __tablename__ = 'integration_connections'

    id = Column(String, primary_key=True, default=generate_uuid)
    service_name = Column(String(100), nullable=False)  # gmail, calendar, crm, project_management
    user_id = Column(String(255), nullable=False)  # email or identifier
    connection_status = Column(String(20), default='pending_auth')  # connected, disconnected, error, pending_auth
    auth_token = Column(Text)  # encrypted
    refresh_token = Column(Text)  # encrypted, optional
    token_expires_at = Column(DateTime)
    scopes = Column(JSON)  # permissions granted
    last_sync_at = Column(DateTime)
    sync_frequency_minutes = Column(Integer, default=15)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    connection_metadata = Column(JSON)  # service-specific configuration

class Notification(Base):
    """
    Notification model for enhanced notification system
    """
    __tablename__ = 'notifications'

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String(255), nullable=False)  # email or identifier
    notification_type = Column(String(30))  # task_completed, approval_needed, system_alert, analytics_report, integration_error
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(10), default='medium')  # low, medium, high, critical
    status = Column(String(20), default='pending')  # pending, sent, delivered, read, failed
    delivery_method = Column(String(20))  # email, sms, push, dashboard, slack
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    read_at = Column(DateTime)
    related_entity_id = Column(String)  # optional, foreign key to related entity
    related_entity_type = Column(String(50))  # optional, type of related entity
    created_at = Column(DateTime, default=datetime.utcnow)

class LearningModel(Base):
    """
    Learning Model model for adaptive learning data
    """
    __tablename__ = 'learning_models'

    id = Column(String, primary_key=True, default=generate_uuid)
    model_type = Column(String(100), nullable=False)  # preference_learning, task_classification, response_generation
    user_id = Column(String(255), nullable=False)  # email or identifier
    model_version = Column(String(20), nullable=False)
    training_data_size = Column(Integer, default=0)
    accuracy_score = Column(Float)
    last_trained_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    model_parameters = Column(JSON)  # algorithm-specific parameters
    performance_metrics = Column(JSON)  # accuracy, precision, recall, etc.
    feature_importance = Column(JSON)  # which factors influence decisions most

def init_db(database_url: str = "sqlite:///silver_tier.db"):
    """
    Initialize the database with all tables
    """
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal, engine

# Global session factory and engine (will be initialized when needed)
SessionLocal = None
engine = None

def get_db_session():
    """
    Get a database session (to be used with dependency injection in FastAPI)
    """
    global SessionLocal
    if SessionLocal is None:
        SessionLocal, _ = init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage:
if __name__ == "__main__":
    # Initialize the database
    session_factory, db_engine = init_db()
    print("Database initialized with all Silver Tier models")

    # Create a sample task
    db = session_factory()
    try:
        # This would be used to create sample data for testing
        pass
    finally:
        db.close()
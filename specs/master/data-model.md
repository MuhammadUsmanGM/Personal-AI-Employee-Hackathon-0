# Data Model - Silver Tier Personal AI Employee System

## Overview
Data model for the enhanced Personal AI Employee system in Silver Tier. This extends the Bronze Tier file-based approach with additional data structures for analytics, learning, and advanced features while maintaining backward compatibility.

## Core Entities

### 1. Task (Enhanced)
**Extension of Bronze Tier Task entity**

```yaml
Task:
  id: UUID (primary key)
  title: String
  description: Text
  status: Enum('pending', 'processing', 'completed', 'failed', 'awaiting_approval')
  priority: Enum('low', 'medium', 'high', 'critical')
  category: String (email, file, calendar, crm, custom)
  source: String (gmail, whatsapp, filesystem, calendar, api)
  created_at: DateTime
  updated_at: DateTime
  due_date: DateTime (optional)
  assigned_to: String (AI, human, team)
  completed_at: DateTime (optional)
  metadata: JSON (source-specific data)
  parent_task_id: UUID (foreign key to Task, optional)
  estimated_duration: Integer (minutes, optional)
  actual_duration: Integer (minutes, optional)
  confidence_score: Float (0-1, AI's confidence in completion)
  retry_count: Integer (default 0)
  last_error: String (optional, for failed tasks)
```

### 2. ApprovalRequest (Enhanced)
**Extension of Bronze Tier Approval entity**

```yaml
ApprovalRequest:
  id: UUID (primary key)
  task_id: UUID (foreign key to Task)
  requester: String (email or system)
  approver: String (email or system)
  reason: Text
  created_at: DateTime
  expires_at: DateTime
  status: Enum('pending', 'approved', 'rejected', 'expired')
  approval_level: Enum('manager', 'director', 'executive')
  business_impact: Enum('low', 'medium', 'high', 'critical')
  financial_impact_amount: Decimal (optional)
  financial_impact_currency: String (optional)
  escalation_required: Boolean (default false)
  escalation_reason: String (optional)
  approved_by: String (email, optional)
  approved_at: DateTime (optional)
  rejected_by: String (email, optional)
  rejected_at: DateTime (optional)
```

### 3. UserPreference (NEW)
**Learning and adaptation preferences**

```yaml
UserPreference:
  id: UUID (primary key)
  user_id: String (email or identifier)
  preference_key: String (e.g., "email_response_style", "approval_threshold", "notification_frequency")
  preference_value: String (JSON serialized for complex values)
  preference_type: Enum('behavioral', 'operational', 'security', 'communication')
  created_at: DateTime
  updated_at: DateTime
  confidence_level: Float (0-1, how certain the system is about this preference)
  usage_count: Integer (how many times this preference has been applied)
  effectiveness_score: Float (-1 to 1, positive if good, negative if bad)
```

### 4. InteractionLog (NEW)
**Tracking all interactions for learning**

```yaml
InteractionLog:
  id: UUID (primary key)
  user_id: String (email or identifier)
  interaction_type: Enum('approval', 'correction', 'feedback', 'override', 'query')
  task_id: UUID (foreign key to Task, optional)
  action_taken: String (description of user action)
  system_response: String (description of system behavior)
  timestamp: DateTime
  context_snapshot: JSON (system state at time of interaction)
  outcome: Enum('positive', 'negative', 'neutral')
  feedback_text: Text (optional, user feedback)
  learning_applied: Boolean (whether this influenced future behavior)
```

### 5. AnalyticsSnapshot (NEW)
**Performance and usage analytics**

```yaml
AnalyticsSnapshot:
  id: UUID (primary key)
  snapshot_time: DateTime
  metric_name: String (e.g., "tasks_processed", "approval_rate", "response_time")
  metric_value: Float
  metric_unit: String (e.g., "count", "percentage", "seconds", "bytes")
  dimension_labels: JSON (tags like {"category": "email", "priority": "high"})
  calculated_from: String (source of calculation)
```

### 6. IntegrationConnection (NEW)
**External service integration connections**

```yaml
IntegrationConnection:
  id: UUID (primary key)
  service_name: String (e.g., "gmail", "calendar", "crm", "project_management")
  user_id: String (email or identifier)
  connection_status: Enum('connected', 'disconnected', 'error', 'pending_auth')
  auth_token: String (encrypted)
  refresh_token: String (encrypted, optional)
  token_expires_at: DateTime (optional)
  scopes: Array<String> (permissions granted)
  last_sync_at: DateTime (optional)
  sync_frequency_minutes: Integer (default 15)
  created_at: DateTime
  updated_at: DateTime
  metadata: JSON (service-specific configuration)
```

### 7. Notification (NEW)
**Enhanced notification system**

```yaml
Notification:
  id: UUID (primary key)
  user_id: String (email or identifier)
  notification_type: Enum('task_completed', 'approval_needed', 'system_alert', 'analytics_report', 'integration_error')
  title: String
  message: Text
  priority: Enum('low', 'medium', 'high', 'critical')
  status: Enum('pending', 'sent', 'delivered', 'read', 'failed')
  delivery_method: Enum('email', 'sms', 'push', 'dashboard', 'slack')
  scheduled_at: DateTime
  sent_at: DateTime (optional)
  read_at: DateTime (optional)
  related_entity_id: UUID (optional, foreign key to related entity)
  related_entity_type: String (optional, type of related entity)
  created_at: DateTime
```

### 8. LearningModel (NEW)
**Adaptive learning data**

```yaml
LearningModel:
  id: UUID (primary key)
  model_type: String (e.g., "preference_learning", "task_classification", "response_generation")
  user_id: String (email or identifier)
  model_version: String
  training_data_size: Integer
  accuracy_score: Float
  last_trained_at: DateTime
  is_active: Boolean (default true)
  model_parameters: JSON (algorithm-specific parameters)
  performance_metrics: JSON (accuracy, precision, recall, etc.)
  feature_importance: JSON (which factors influence decisions most)
```

## Relationships

### Task Relationships
- Task may have parent Task (for hierarchical tasks)
- Task connects to ApprovalRequest (one-to-one, optional)
- Task connects to InteractionLog (one-to-many)

### ApprovalRequest Relationships
- ApprovalRequest connects to Task (many-to-one)
- ApprovalRequest connects to UserPreference (through approval level preferences)

### UserPreference Relationships
- UserPreference connects to InteractionLog (one-to-many)
- UserPreference connects to LearningModel (one-to-many)

### System Relationships
- IntegrationConnection connects to User (many-to-one)
- Notification connects to User (many-to-one)
- AnalyticsSnapshot connects to various entities through dimension_labels

## State Transitions

### Task State Transitions
```
pending → processing → completed
pending → processing → awaiting_approval → (approved → processing → completed) or (rejected → failed)
pending → processing → failed → (retry → processing) or (manual_intervention)
```

### ApprovalRequest State Transitions
```
pending → approved → completed
pending → rejected → completed
pending → expired
```

### IntegrationConnection State Transitions
```
pending_auth → connected → disconnected → connected
connected → error → connected
connected → disconnected
```

## Indexes for Performance

### Task Table
- idx_task_status (status)
- idx_task_assigned_to (assigned_to)
- idx_task_category (category)
- idx_task_created_at (created_at)
- idx_task_due_date (due_date)

### ApprovalRequest Table
- idx_approval_request_status (status)
- idx_approval_request_created_at (created_at)
- idx_approval_request_expires_at (expires_at)

### InteractionLog Table
- idx_interaction_log_user_id (user_id)
- idx_interaction_log_timestamp (timestamp)
- idx_interaction_log_type (interaction_type)

### AnalyticsSnapshot Table
- idx_analytics_snapshot_time (snapshot_time)
- idx_analytics_snapshot_name (metric_name)
- idx_analytics_snapshot_composite (snapshot_time, metric_name)
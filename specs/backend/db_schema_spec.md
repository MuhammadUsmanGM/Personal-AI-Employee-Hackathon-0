# Database Schema Specification for Personal AI Employee

## Overview
This document defines the complete database schema for the Personal AI Employee system, including tables, relationships, indexes, and constraints.

## Database Configuration

### Database Engine
- **Primary**: PostgreSQL 15+ for production
- **Development**: SQLite 3.38+ for local development
- **Caching**: Redis 7+ for session and cache

### Connection Pooling
- **Pool Size**: 20 connections for production
- **Idle Timeout**: 300 seconds
- **Connection Timeout**: 30 seconds

## Core Tables

### 1. Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    status VARCHAR(20) DEFAULT 'active',
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    preferences JSONB DEFAULT '{}',
    CONSTRAINT chk_role CHECK (role IN ('admin', 'user', 'observer')),
    CONSTRAINT chk_status CHECK (status IN ('active', 'inactive', 'suspended'))
);
```

### 2. Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    assigned_to UUID REFERENCES users(id),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    completed_at TIMESTAMP,
    estimated_duration INTEGER, -- in minutes
    actual_duration INTEGER,    -- in minutes
    metadata JSONB DEFAULT '{}',
    dependencies UUID[], -- array of task IDs this task depends on
    tags TEXT[],
    CONSTRAINT chk_status CHECK (status IN ('pending', 'in_progress', 'completed', 'failed', 'cancelled')),
    CONSTRAINT chk_priority CHECK (priority IN ('low', 'medium', 'high', 'critical'))
);
```

### 3. Approvals Table
```sql
CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    action_type VARCHAR(100) NOT NULL,
    details JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    requested_by VARCHAR(100), -- could be user_id or system identifier
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMP,
    rejected_by UUID REFERENCES users(id),
    rejected_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    CONSTRAINT chk_approval_status CHECK (status IN ('pending', 'approved', 'rejected', 'expired'))
);
```

### 4. System Logs Table
```sql
CREATE TABLE system_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(20) NOT NULL,
    module VARCHAR(100),
    message TEXT,
    user_id UUID REFERENCES users(id),
    task_id UUID REFERENCES tasks(id),
    request_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    metadata JSONB,
    CONSTRAINT chk_log_level CHECK (level IN ('debug', 'info', 'warning', 'error', 'critical'))
);
```

### 5. MCP Server Configurations Table
```sql
CREATE TABLE mcp_servers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    server_type VARCHAR(50) NOT NULL,
    command TEXT NOT NULL,
    args TEXT[],
    environment JSONB,
    status VARCHAR(20) DEFAULT 'inactive',
    last_heartbeat TIMESTAMP,
    capabilities TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    CONSTRAINT chk_server_status CHECK (status IN ('active', 'inactive', 'error'))
);
```

### 6. Watcher Configurations Table
```sql
CREATE TABLE watchers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    watcher_type VARCHAR(50) NOT NULL,
    config JSONB,
    is_active BOOLEAN DEFAULT true,
    last_run TIMESTAMP,
    last_error TEXT,
    error_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id)
);
```

### 7. Sessions Table
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    is_revoked BOOLEAN DEFAULT false
);
```

### 8. File Attachments Table
```sql
CREATE TABLE file_attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100),
    file_size BIGINT,
    storage_path TEXT NOT NULL,
    uploaded_by UUID REFERENCES users(id),
    task_id UUID REFERENCES tasks(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_encrypted BOOLEAN DEFAULT false,
    hash_checksum VARCHAR(64) -- SHA-256 hash
);
```

### 9. Notifications Table
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    message TEXT,
    type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    status VARCHAR(20) DEFAULT 'unread',
    data JSONB,
    read_at TIMESTAMP,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scheduled_for TIMESTAMP,
    channel VARCHAR(50) DEFAULT 'web',
    CONSTRAINT chk_notification_type CHECK (type IN ('alert', 'approval', 'status', 'error', 'info')),
    CONSTRAINT chk_notification_status CHECK (status IN ('unread', 'read', 'archived')),
    CONSTRAINT chk_notification_channel CHECK (channel IN ('web', 'email', 'push', 'sms'))
);
```

### 10. Audit Trail Table
```sql
CREATE TABLE audit_trail (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Indexes

### Primary Indexes
```sql
-- Users table indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- Tasks table indexes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Approvals table indexes
CREATE INDEX idx_approvals_status ON approvals(status);
CREATE INDEX idx_approvals_task_id ON approvals(task_id);
CREATE INDEX idx_approvals_expires_at ON approvals(expires_at);

-- System logs table indexes
CREATE INDEX idx_system_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX idx_system_logs_level ON system_logs(level);
CREATE INDEX idx_system_logs_module ON system_logs(module);

-- Sessions table indexes
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

-- File attachments indexes
CREATE INDEX idx_file_attachments_task_id ON file_attachments(task_id);
CREATE INDEX idx_file_attachments_uploaded_by ON file_attachments(upload_by);
```

### Composite Indexes
```sql
-- Task filtering combinations
CREATE INDEX idx_tasks_status_priority ON tasks(status, priority);
CREATE INDEX idx_tasks_assigned_status ON tasks(assigned_to, status);
CREATE INDEX idx_tasks_user_status ON tasks(created_by, status);

-- Approval filtering
CREATE INDEX idx_approvals_status_requested ON approvals(status, requested_by);
CREATE INDEX idx_approvals_user_status ON approvals(approved_by, status);

-- Log filtering
CREATE INDEX idx_system_logs_user_timestamp ON system_logs(user_id, timestamp DESC);
CREATE INDEX idx_system_logs_module_level ON system_logs(module, level);
```

### Full-Text Search Indexes
```sql
-- For searching in task descriptions and titles
CREATE INDEX idx_tasks_fulltext ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));

-- For searching in log messages
CREATE INDEX idx_logs_fulltext ON system_logs USING gin(to_tsvector('english', message));
```

## Constraints and Triggers

### Check Constraints
```sql
-- Ensure due_date is not in the past for completed tasks
ALTER TABLE tasks ADD CONSTRAINT chk_due_date_not_past
CHECK (status != 'completed' OR due_date >= CURRENT_DATE);

-- Ensure only one approval status is set
ALTER TABLE approvals ADD CONSTRAINT chk_approval_single_decision
CHECK ((approved_by IS NOT NULL AND rejected_by IS NULL) OR
       (approved_by IS NULL AND rejected_by IS NOT NULL) OR
       (approved_by IS NULL AND rejected_by IS NULL));

-- Ensure priority duration correlation
ALTER TABLE tasks ADD CONSTRAINT chk_priority_duration
CHECK (priority != 'critical' OR estimated_duration <= 1440); -- 24 hours max for critical
```

### Row-Level Security
```sql
-- Enable RLS on sensitive tables
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE approvals ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_logs ENABLE ROW LEVEL SECURITY;

-- Policies for tasks
CREATE POLICY user_can_view_own_tasks ON tasks
    FOR SELECT TO app_user
    USING (created_by = current_user_id());

CREATE POLICY user_can_modify_assigned_tasks ON tasks
    FOR ALL TO app_user
    USING (assigned_to = current_user_id());
```

## Views

### Task Summary View
```sql
CREATE VIEW task_summary AS
SELECT
    t.id,
    t.title,
    t.status,
    t.priority,
    u.username as assigned_to_name,
    t.created_at,
    t.updated_at,
    t.due_date,
    COUNT(a.id) as approval_requests,
    CASE
        WHEN t.due_date < CURRENT_DATE THEN 'overdue'
        WHEN t.due_date <= CURRENT_DATE + INTERVAL '1 day' THEN 'due_soon'
        ELSE 'on_track'
    END as urgency_status
FROM tasks t
LEFT JOIN users u ON t.assigned_to = u.id
LEFT JOIN approvals a ON t.id = a.task_id
GROUP BY t.id, u.username;
```

### Daily Activity View
```sql
CREATE VIEW daily_activity AS
SELECT
    DATE(l.timestamp) as activity_date,
    l.level,
    COUNT(*) as event_count,
    STRING_AGG(DISTINCT l.module, ', ') as modules_affected
FROM system_logs l
WHERE l.timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(l.timestamp), l.level
ORDER BY activity_date DESC, l.level;
```

## Stored Procedures and Functions

### Task Assignment Function
```sql
CREATE OR REPLACE FUNCTION assign_task(
    p_task_id UUID,
    p_assignee_id UUID,
    p_current_user_id UUID
) RETURNS VOID AS $$
BEGIN
    -- Check if user has permission to assign tasks
    IF NOT has_permission(p_current_user_id, 'task_assign') THEN
        RAISE EXCEPTION 'Permission denied: Cannot assign tasks';
    END IF;

    UPDATE tasks
    SET assigned_to = p_assignee_id, updated_at = CURRENT_TIMESTAMP
    WHERE id = p_task_id;

    -- Log the assignment
    INSERT INTO audit_trail (user_id, action, entity_type, entity_id, new_values)
    VALUES (p_current_user_id, 'task_assigned', 'task', p_task_id,
            json_build_object('assigned_to', p_assignee_id));
END;
$$ LANGUAGE plpgsql;
```

### Cleanup Expired Sessions
```sql
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM sessions WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Schedule for daily execution
SELECT cron.schedule('cleanup-sessions', '0 2 * * *', $$SELECT cleanup_expired_sessions();$$);
```

## Partitioning Strategy

### System Logs Partitioning
```sql
-- Create partitioned table for logs
CREATE TABLE system_logs_partitioned (
    LIKE system_logs INCLUDING ALL
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE system_logs_2026_01 PARTITION OF system_logs_partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE system_logs_2026_02 PARTITION OF system_logs_partitioned
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Continue for remaining months...
```

## Backup and Recovery

### Backup Strategy
```sql
-- Configuration for pg_dump
-- Daily full backup at 2 AM
-- Transaction log shipping for point-in-time recovery
-- Offsite backup storage with encryption
```

### Recovery Procedures
```sql
-- Point-in-time recovery script
-- Restore from latest full backup
-- Apply transaction logs up to target time
-- Verify data integrity
```

## Performance Optimization

### Query Optimization
- Use prepared statements for repeated queries
- Implement connection pooling
- Use appropriate isolation levels
- Optimize for read-heavy workloads

### Maintenance Tasks
- Regular vacuum and analyze
- Index rebuilding as needed
- Statistics updates
- Constraint validation
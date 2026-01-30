# API Routes Specification for Personal AI Employee

## Overview
This document defines all API routes for the Personal AI Employee system, including authentication, task management, approvals, monitoring, and integration endpoints.

## Base Configuration

### API Base URL
```
Base URL: https://api.ai-employee.com/v1 or http://localhost:8000/v1
Version: v1
Content-Type: application/json
```

### Common Headers
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
X-Request-ID: {unique_request_id}
Accept: application/json
```

## Authentication Routes

### Login
```
POST /auth/login
```
**Description**: Authenticate user and return JWT token

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "access_token": "jwt_token",
    "refresh_token": "refresh_token",
    "expires_in": 3600,
    "user": {
      "id": "user_id",
      "username": "username",
      "role": "admin|user|observer"
    }
  },
  "message": "Login successful",
  "timestamp": "2026-01-07T10:30:00Z"
}
```

### Refresh Token
```
POST /auth/refresh
```
**Description**: Refresh expired access token

**Headers**:
```
Authorization: Bearer {refresh_token}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "access_token": "new_jwt_token",
    "expires_in": 3600
  }
}
```

### Logout
```
POST /auth/logout
```
**Description**: Invalidate current session

**Response**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

## Task Management Routes

### Get All Tasks
```
GET /tasks
```
**Description**: Retrieve list of tasks with filtering and pagination

**Query Parameters**:
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `status` (optional): Filter by status (pending, in_progress, completed, failed)
- `priority` (optional): Filter by priority (low, medium, high, critical)
- `assigned_to` (optional): Filter by assignee
- `sort_by` (optional): Sort field (created_at, updated_at, priority)
- `order` (optional): Sort order (asc, desc)

**Response**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "task_id",
        "title": "Task title",
        "description": "Task description",
        "status": "pending|in_progress|completed|failed",
        "priority": "low|medium|high|critical",
        "assigned_to": "user_id",
        "created_at": "2026-01-07T10:30:00Z",
        "updated_at": "2026-01-07T10:30:00Z",
        "due_date": "2026-01-08T10:30:00Z",
        "metadata": {}
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

### Create Task
```
POST /tasks
```
**Description**: Create a new task

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Task description",
  "priority": "medium",
  "assigned_to": "user_id",
  "due_date": "2026-01-08T10:30:00Z",
  "metadata": {}
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "new_task_id",
    "title": "Task title",
    "description": "Task description",
    "status": "pending",
    "priority": "medium",
    "assigned_to": "user_id",
    "created_at": "2026-01-07T10:30:00Z",
    "updated_at": "2026-01-07T10:30:00Z",
    "due_date": "2026-01-08T10:30:00Z",
    "metadata": {}
  },
  "message": "Task created successfully"
}
```

### Get Task by ID
```
GET /tasks/{task_id}
```
**Description**: Retrieve specific task by ID

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "task_id",
    "title": "Task title",
    "description": "Task description",
    "status": "pending",
    "priority": "medium",
    "assigned_to": "user_id",
    "created_at": "2026-01-07T10:30:00Z",
    "updated_at": "2026-01-07T10:30:00Z",
    "due_date": "2026-01-08T10:30:00Z",
    "metadata": {},
    "steps": [
      {
        "id": "step_id",
        "description": "Step description",
        "status": "pending|completed",
        "completed_at": "2026-01-07T10:30:00Z"
      }
    ]
  }
}
```

### Update Task
```
PUT /tasks/{task_id}
```
**Description**: Update existing task

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "high",
  "assigned_to": "new_user_id",
  "due_date": "2026-01-09T10:30:00Z",
  "metadata": {}
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "task_id",
    "title": "Updated title",
    "description": "Updated description",
    "status": "in_progress",
    "priority": "high",
    "assigned_to": "new_user_id",
    "updated_at": "2026-01-07T10:30:00Z",
    "due_date": "2026-01-09T10:30:00Z",
    "metadata": {}
  },
  "message": "Task updated successfully"
}
```

### Update Task Status
```
PATCH /tasks/{task_id}/status
```
**Description**: Update only the status of a task

**Request Body**:
```json
{
  "status": "completed|failed|in_progress"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "task_id",
    "status": "completed",
    "updated_at": "2026-01-07T10:30:00Z"
  },
  "message": "Task status updated successfully"
}
```

### Delete Task
```
DELETE /tasks/{task_id}
```
**Description**: Delete a task

**Response**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

## Approval Management Routes

### Get Pending Approvals
```
GET /approvals
```
**Description**: Retrieve list of pending approvals

**Query Parameters**:
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `status` (optional): Filter by status (pending, approved, rejected)
- `action_type` (optional): Filter by action type

**Response**:
```json
{
  "success": true,
  "data": {
    "approvals": [
      {
        "id": "approval_id",
        "task_id": "task_id",
        "action_type": "payment|email_send|social_post",
        "details": {
          "amount": 500.00,
          "recipient": "Client A",
          "description": "Invoice #123 payment"
        },
        "status": "pending",
        "requested_by": "claude_code",
        "created_at": "2026-01-07T10:30:00Z",
        "expires_at": "2026-01-08T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 5,
      "pages": 1
    }
  }
}
```

### Create Approval Request
```
POST /approvals
```
**Description**: Create a new approval request

**Request Body**:
```json
{
  "task_id": "task_id",
  "action_type": "payment",
  "details": {
    "amount": 500.00,
    "recipient": "Client A",
    "description": "Invoice #123 payment"
  },
  "expires_at": "2026-01-08T10:30:00Z"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "new_approval_id",
    "task_id": "task_id",
    "action_type": "payment",
    "details": {
      "amount": 500.00,
      "recipient": "Client A",
      "description": "Invoice #123 payment"
    },
    "status": "pending",
    "requested_by": "claude_code",
    "created_at": "2026-01-07T10:30:00Z",
    "expires_at": "2026-01-08T10:30:00Z"
  },
  "message": "Approval request created successfully"
}
```

### Update Approval Status
```
PUT /approvals/{approval_id}
```
**Description**: Approve or reject an approval request

**Request Body**:
```json
{
  "status": "approved|rejected",
  "notes": "Optional notes about the decision"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "approval_id",
    "status": "approved",
    "approved_by": "user_id",
    "approved_at": "2026-01-07T10:35:00Z",
    "notes": "Optional notes about the decision"
  },
  "message": "Approval updated successfully"
}
```

## Status and Monitoring Routes

### System Status
```
GET /status
```
**Description**: Get overall system health status

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-01-07T10:30:00Z",
    "services": {
      "database": "healthy",
      "redis": "healthy",
      "mcp_servers": "healthy",
      "storage": "healthy"
    },
    "metrics": {
      "active_tasks": 3,
      "pending_approvals": 1,
      "uptime": 86400,
      "cpu_usage": 15.2,
      "memory_usage": 45.6
    }
  }
}
```

### System Metrics
```
GET /status/metrics
```
**Description**: Get detailed system metrics

**Response**:
```json
{
  "success": true,
  "data": {
    "performance": {
      "response_time_avg": 150,
      "requests_per_minute": 45,
      "error_rate": 0.02
    },
    "resources": {
      "cpu_usage": 15.2,
      "memory_usage": 45.6,
      "disk_usage": 65.3,
      "network_io": 1024
    },
    "application": {
      "active_users": 1,
      "active_tasks": 3,
      "pending_approvals": 1,
      "completed_today": 12
    }
  }
}
```

### Get Logs
```
GET /logs
```
**Description**: Retrieve system logs with filtering

**Query Parameters**:
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 50, max: 200)
- `level` (optional): Filter by log level (debug, info, warning, error, critical)
- `module` (optional): Filter by module name
- `start_date` (optional): Filter from date (ISO 8601)
- `end_date` (optional): Filter to date (ISO 8601)

**Response**:
```json
{
  "success": true,
  "data": {
    "logs": [
      {
        "id": "log_id",
        "timestamp": "2026-01-07T10:30:00Z",
        "level": "info",
        "module": "task_manager",
        "message": "Task completed successfully",
        "metadata": {
          "task_id": "task_id",
          "result": "success"
        }
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 50,
      "total": 100,
      "pages": 2
    }
  }
}
```

## Configuration Routes

### Get Configuration
```
GET /config
```
**Description**: Get system configuration

**Response**:
```json
{
  "success": true,
  "data": {
    "general": {
      "timezone": "UTC",
      "language": "en",
      "date_format": "YYYY-MM-DD"
    },
    "security": {
      "password_policy": {
        "min_length": 8,
        "require_special_chars": true
      },
      "session_timeout": 3600
    },
    "integrations": {
      "gmail_enabled": true,
      "whatsapp_enabled": true,
      "banking_enabled": false
    }
  }
}
```

### Update Configuration
```
PUT /config
```
**Description**: Update system configuration

**Request Body**:
```json
{
  "general": {
    "timezone": "America/New_York"
  },
  "security": {
    "session_timeout": 7200
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "general": {
      "timezone": "America/New_York",
      "language": "en",
      "date_format": "YYYY-MM-DD"
    },
    "security": {
      "password_policy": {
        "min_length": 8,
        "require_special_chars": true
      },
      "session_timeout": 7200
    },
    "integrations": {
      "gmail_enabled": true,
      "whatsapp_enabled": true,
      "banking_enabled": false
    }
  },
  "message": "Configuration updated successfully"
}
```

## MCP Integration Routes

### Execute MCP Action
```
POST /mcp/execute
```
**Description**: Execute an action through MCP server

**Request Body**:
```json
{
  "server_name": "email",
  "action": "send_email",
  "parameters": {
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email"
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "result": "success",
    "execution_id": "exec_id",
    "timestamp": "2026-01-07T10:30:00Z"
  },
  "message": "MCP action executed successfully"
}
```

### Get MCP Status
```
GET /mcp/status
```
**Description**: Get status of all MCP servers

**Response**:
```json
{
  "success": true,
  "data": {
    "servers": [
      {
        "name": "email",
        "status": "connected",
        "capabilities": ["send_email", "draft_email"],
        "last_heartbeat": "2026-01-07T10:30:00Z"
      },
      {
        "name": "browser",
        "status": "connected",
        "capabilities": ["navigate", "click", "fill_form"],
        "last_heartbeat": "2026-01-07T10:29:55Z"
      }
    ]
  }
}
```

## Error Responses

### Common Error Formats

**Unauthorized** (401):
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

**Forbidden** (403):
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions"
  }
}
```

**Not Found** (404):
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

**Validation Error** (422):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

**Rate Limited** (429):
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "retry_after": 60
  }
}
```

**Internal Server Error** (500):
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An internal server error occurred"
  }
}
```

## Webhook Endpoints

### Task Status Update Webhook
```
POST /webhooks/task-status
```
**Description**: Receive task status updates from external systems

**Headers**:
```
X-Webhook-Signature: sha256=signature
```

**Request Body**:
```json
{
  "task_id": "task_id",
  "status": "completed",
  "result": "success",
  "timestamp": "2026-01-07T10:30:00Z"
}
```

## WebSocket Endpoints

### Real-time Updates
```
/ws/updates
```
**Description**: WebSocket connection for real-time updates

**Supported Messages**:
- `task_created`: New task created
- `task_updated`: Task status changed
- `approval_needed`: New approval required
- `system_alert`: System alert or error

**Message Format**:
```json
{
  "type": "task_updated",
  "data": {
    "task_id": "task_id",
    "status": "completed"
  },
  "timestamp": "2026-01-07T10:30:00Z"
}
```

## Rate Limiting

### Limits Per Endpoint
- Authentication: 10 requests/minute per IP
- Task Management: 100 requests/minute per user
- Approval Management: 50 requests/minute per user
- Status/Monitoring: 200 requests/minute per user
- MCP Integration: 30 requests/minute per user

### Burst Limits
- Authentication: 5 requests in 1 second
- All other endpoints: 20 requests in 10 seconds
# System Integration Specification for Personal AI Employee

## Overview
This document defines how all components of the Personal AI Employee system integrate with each other, including data flow, communication protocols, and inter-service dependencies.

## System Architecture Integration

### Component Interactions
```
External Sources → Watchers → Obsidian Vault → Claude Code → MCP Servers → External Systems
     ↓              ↓            ↓            ↓           ↓         ↓
   Gmail,     Creates .md    Processes    Makes      Executes   Completes
  WhatsApp,   files in      tasks via     decisions   external   tasks,
  Banking    Needs_Action   claude code   & plans     actions    logs results

                    ↑
                Dashboard ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### Data Flow Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   External      │    │   Watcher       │    │  Obsidian       │
│   Sources       │───▶│   Services      │───▶│  Vault          │
│ (Gmail,        │    │ (Python)        │    │ (Markdown)      │
│ WhatsApp,      │    │                 │    │                 │
│ Banking)       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐             │
│   MCP Servers   │◀───│  Claude Code    │◀────────────┘
│ (Node.js)       │    │ (Reasoning)     │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
```

## Integration Points

### 1. Watcher → Obsidian Integration

#### File Creation Protocol
- **Location**: `/Needs_Action/` directory
- **Format**: Markdown with YAML frontmatter
- **Naming Convention**: `{SOURCE}_{IDENTIFIER}_{TIMESTAMP}.md`
- **Content Structure**:
  ```markdown
  ---
  type: email|whatsapp|file_drop|finance
  source: gmail|whatsapp|filesystem|banking
  priority: low|medium|high|critical
  status: pending
  created: 2026-01-07T10:30:00Z
  ---
  ## Content
  Original content or extracted information

  ## Suggested Actions
  - [ ] Action item 1
  - [ ] Action item 2
  ```

#### Error Handling
- Retry failed file creations with exponential backoff
- Log errors to `/Logs/watcher_errors_{DATE}.json`
- Alert system administrators for persistent failures

### 2. Claude Code → Obsidian Integration

#### File Reading Protocol
- **Scan Directory**: `/Needs_Action/` every 30 seconds
- **Process Order**: Priority-based (critical → high → medium → low)
- **Lock Mechanism**: Prevent duplicate processing using temporary lock files
- **Status Updates**: Update file status in real-time

#### File Writing Protocol
- **Plan Creation**: Write to `/Plans/PLAN_{TYPE}_{ID}.md`
- **Dashboard Updates**: Update `/Dashboard.md` with current status
- **Approval Requests**: Create in `/Pending_Approval/APPROVAL_{ACTION}_{ID}.md`
- **Completion**: Move processed files to `/Done/{ORIGINAL_NAME}.md`

### 3. Claude Code → MCP Server Integration

#### Communication Protocol
- **Transport**: MCP (Model Context Protocol) over TCP/IPC
- **Serialization**: JSON-RPC 2.0
- **Authentication**: API key validation
- **Timeout**: 30 seconds per request

#### Request Format
```json
{
  "jsonrpc": "2.0",
  "method": "send_email",
  "params": {
    "to": "recipient@example.com",
    "subject": "Email Subject",
    "body": "Email body content",
    "attachments": []
  },
  "id": "request_id"
}
```

#### Response Format
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "data": {},
    "execution_id": "exec_id"
  },
  "id": "request_id"
}
```

### 4. MCP Server → External Systems Integration

#### API Communication
- **Protocols**: REST API, GraphQL, SMTP, IMAP
- **Authentication**: OAuth 2.0, API keys, JWT tokens
- **Rate Limiting**: Respect external service limits
- **Retry Logic**: Exponential backoff for transient failures

#### Security Measures
- **Credential Isolation**: Store credentials separately from vault
- **Network Segmentation**: Use VPN or private networks
- **Certificate Pinning**: For critical connections
- **Audit Logging**: Log all external communications

## Event-Driven Architecture

### Message Queues
- **Technology**: Redis Streams or RabbitMQ
- **Queues**:
  - `task_queue`: For incoming tasks
  - `approval_queue`: For approval requests
  - `notification_queue`: For user notifications
  - `mcp_queue`: For MCP server requests

### Event Types
```typescript
interface SystemEvent {
  eventId: string;
  eventType: 'task.created' | 'task.completed' | 'approval.requested' | 'system.alert';
  timestamp: Date;
  source: string;
  payload: any;
  correlationId?: string;
}
```

### Event Processing
```python
# Event processor example
class EventHandler:
    def handle_task_completed(self, event: SystemEvent):
        # Update dashboard
        self.dashboard_service.update_status()

        # Check for dependent tasks
        self.task_service.release_dependent_tasks(event.payload.task_id)

        # Log completion
        self.logging_service.log_completion(event)
```

## Real-time Communication

### WebSocket Integration
- **Endpoint**: `/ws/updates`
- **Authentication**: JWT token validation
- **Message Types**:
  - `task_update`: Task status changes
  - `approval_needed`: New approval required
  - `system_alert`: System health alerts
  - `progress_update`: Long-running task progress

### Server-Sent Events (SSE)
- **Endpoint**: `/events/stream`
- **Use Cases**: Dashboard live updates, progress indicators
- **Fallback**: Polling for older browsers

## API Gateway Integration

### Request Routing
```
Client Request → API Gateway → Authentication → Rate Limiting → Service Discovery → Target Service
```

### Middleware Chain
1. **Authentication**: Validate JWT tokens
2. **Rate Limiting**: Apply per-user limits
3. **Validation**: Validate request schemas
4. **Logging**: Log request metadata
5. **Caching**: Serve cached responses when possible
6. **Forward**: Route to appropriate service

### Response Handling
- **Standardization**: Wrap all responses in common format
- **Error Handling**: Convert service errors to standard format
- **Compression**: Compress responses >1KB
- **CORS**: Handle cross-origin requests appropriately

## Data Synchronization

### Local-Cloud Sync (Platinum Tier)
- **Technology**: Git-based synchronization
- **Frequency**: Real-time for critical data, periodic for bulk data
- **Conflict Resolution**: Last-write-wins with manual override
- **Exclusions**: Secrets, credentials, sensitive data never sync

### Sync Process
```bash
# Sync script example
#!/bin/bash
# Exclude sensitive files
rsync -av \
  --exclude=".env*" \
  --exclude="*.session" \
  --exclude="credentials.json" \
  --exclude="tokens/" \
  ./vault/ user@cloud:/backup/vault/
```

## Health Monitoring Integration

### Service Dependencies
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   MCP       │    │  Claude     │    │  Watchers   │
│  Servers    │◄──►│   Code      │◄──►│             │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ External    │    │ Obsidian    │    │ File        │
│ Services    │    │ Vault       │    │ System      │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Health Check Endpoints
- **MCP Servers**: `/health` endpoint with capability checks
- **Claude Code**: MCP connectivity verification
- **Watchers**: Process heartbeat and error monitoring
- **Database**: Connection pool health
- **Redis**: Cache connectivity and performance

### Alerting System
- **Thresholds**: CPU > 80%, Memory > 85%, Disk > 90%
- **Escalation**: PagerDuty for critical alerts
- **Silencing**: Scheduled maintenance windows
- **Grouping**: Related alerts grouped together

## Configuration Management

### Centralized Configuration
```yaml
# config.yaml
system:
  timezone: "UTC"
  locale: "en_US"

obsidian:
  vault_path: "/path/to/vault"
  refresh_interval: 30

mcp_servers:
  email:
    enabled: true
    timeout: 30
  browser:
    enabled: true
    headless: true

watchers:
  gmail:
    check_interval: 120
    enabled: true
  whatsapp:
    check_interval: 30
    enabled: true

security:
  jwt_expiry_hours: 24
  rate_limits:
    api_calls: 100
    window_minutes: 1
```

### Configuration Reload
- **Hot Reload**: Configuration changes applied without restart
- **Validation**: Validate config before applying
- **Rollback**: Automatic rollback on validation failure
- **Audit**: Log all configuration changes

## Error Handling & Recovery

### Circuit Breaker Pattern
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpen("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
```

### Retry Mechanisms
- **Exponential Backoff**: For transient failures
- **Jitter**: Random delay to prevent thundering herd
- **Maximum Attempts**: Configurable retry limits
- **Circuit Breaker**: Prevent cascading failures

## Performance Integration

### Caching Strategy
- **Application Level**: Redis for session and temporary data
- **Database Level**: Query result caching
- **API Level**: Response caching with etags
- **File Level**: Obsidian vault file caching

### Load Balancing
- **Application**: Round-robin for multiple Claude Code instances
- **Database**: Read replicas for query scaling
- **MCP Servers**: Pool of available servers
- **Watchers**: Distributed across multiple machines

## Security Integration

### Zero Trust Architecture
- **Service-to-Service**: Mutual TLS authentication
- **API Keys**: Per-service authentication
- **RBAC**: Role-based access control
- **Audit**: Comprehensive logging of all actions

### Data Encryption
- **At Rest**: AES-256 for stored data
- **In Transit**: TLS 1.3 for all communications
- **Secrets**: Hardware security module (HSM) when available
- **Backups**: Encrypted backup storage

## Testing Integration

### Integration Testing
```python
# Example integration test
def test_complete_workflow():
    # 1. Create test data in Obsidian vault
    task_file = create_test_task()

    # 2. Trigger Claude Code processing
    claude_process.trigger_processing()

    # 3. Verify MCP server interaction
    assert mcp_mock.was_called_with(expected_params)

    # 4. Verify result in Done folder
    assert task_completed_in_done_folder()

    # 5. Verify dashboard update
    assert dashboard_was_updated()
```

### Contract Testing
- **API Contracts**: Validate request/response schemas
- **Event Contracts**: Ensure event format consistency
- **Database Contracts**: Verify schema compatibility
- **MCP Contracts**: Validate protocol compliance

## Deployment Integration

### Blue-Green Deployment
- **Parallel Environments**: Blue and green environments
- **Traffic Switching**: Gradual traffic migration
- **Rollback Capability**: Instant rollback if issues detected
- **Health Verification**: Automated health checks

### Canary Releases
- **Gradual Rollout**: 5% → 25% → 50% → 100% traffic
- **Metrics Monitoring**: Performance and error rate tracking
- **Automatic Rollback**: Rollback on metric threshold breach
- **Feature Flags**: Toggle features without deployment

## Monitoring & Observability

### Metrics Collection
- **Application Metrics**: Response times, error rates, throughput
- **Infrastructure Metrics**: CPU, memory, disk, network
- **Business Metrics**: Task completion rates, approval times
- **Custom Metrics**: Domain-specific KPIs

### Distributed Tracing
- **Trace ID**: Propagate trace ID across services
- **Span Creation**: Create spans for each service call
- **Visualization**: Trace visualization in monitoring tools
- **Analysis**: Identify bottlenecks and performance issues

## Backup & Disaster Recovery

### Data Backup Strategy
- **Vault Backup**: Daily incremental, weekly full
- **Database Backup**: Continuous archiving
- **Configuration Backup**: Version-controlled configs
- **MCP Backup**: Server configuration snapshots

### Recovery Procedures
- **RTO**: Recovery Time Objective - 4 hours
- **RPO**: Recovery Point Objective - 1 hour
- **Failover**: Automated failover procedures
- **Testing**: Regular disaster recovery testing
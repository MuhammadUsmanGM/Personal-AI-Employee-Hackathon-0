# Personal AI Employee - Architecture Specifications

## Overview
The Personal AI Employee is an autonomous digital worker that combines Claude Code as the reasoning engine with Obsidian as the memory/dashboard system. It uses Python watchers for external monitoring and MCP servers for taking actions.

## System Architecture

### Core Components
1. **The Brain**: Claude Code as the reasoning engine
2. **The Memory/GUI**: Obsidian (local Markdown) as dashboard
3. **The Senses**: Python watchers monitoring external inputs
4. **The Hands**: MCP servers for external actions

### Data Flow Architecture
```
External Sources → Watchers → Obsidian Vault → Claude Code → MCP Servers → Actions
     ↓              ↓            ↓            ↓           ↓         ↓
   Gmail,     Creates .md    Processes    Makes      Executes   Completes
  WhatsApp,   files in      tasks via     decisions   external   tasks,
  Banking    Needs_Action   claude code   & plans     actions    logs results
```

## Tiered Implementation

### Bronze Tier: Foundation
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script (Gmail OR file system monitoring)
- Claude Code reading/writing to vault
- Basic folder structure: /Inbox, /Needs_Action, /Done

### Silver Tier: Functional Assistant
- Two or more Watcher scripts (Gmail + WhatsApp + LinkedIn)
- Claude reasoning loop creating Plan.md files
- One working MCP server for external action
- Human-in-the-loop approval workflow
- Basic scheduling

### Gold Tier: Autonomous Employee
- Full cross-domain integration (Personal + Business)
- Accounting system integration (Odoo)
- Social media integration (Facebook, Instagram, Twitter)
- Weekly Business and Accounting Audit
- Error recovery and graceful degradation
- Ralph Wiggum loop for autonomous completion

### Platinum Tier: Always-On Cloud + Local Executive
- 24/7 Cloud deployment
- Work-zone specialization
- Delegation via synced vault
- Direct A2A communication

## Security Architecture

### Credential Management
- Never store credentials in Obsidian vault
- Use environment variables for API keys
- Separate accounts for development/testing
- Monthly credential rotation

### Human-in-the-Loop (HITL)
- Approval files for sensitive actions
- Configurable approval thresholds
- Audit logging for all actions
- Dry-run capability for development

## Technical Requirements

### Hardware
- Minimum: 8GB RAM, 4-core CPU, 20GB free disk space
- Recommended: 16GB RAM, 8-core CPU, SSD storage

### Software Stack
- Claude Code (Pro subscription)
- Obsidian v1.10.6+
- Python 3.13+
- Node.js v24+ LTS
- GitHub Desktop

## Error Handling & Recovery

### Error Categories
- Transient: Network timeouts, API rate limits
- Authentication: Expired tokens, revoked access
- Logic: Misinterpretation of messages
- Data: Corrupted files, missing fields
- System: Process crashes, resource exhaustion

### Recovery Strategies
- Exponential backoff for retries
- Alert human for authentication issues
- Human review queue for logic errors
- Quarantine corrupted data
- Auto-restart for system crashes

## Monitoring & Logging

### Required Log Format
```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "actor": "claude_code",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### Audit Trail Requirements
- Store logs in /Vault/Logs/YYYY-MM-DD.json
- Retain logs for minimum 90 days
- Log all external actions
- Record approval status for all actions

## Performance Requirements

### Response Times
- Watcher check intervals: 30-120 seconds
- Claude processing: Within seconds when triggered
- MCP action execution: Within reasonable timeframes
- Human notification: Immediate for time-sensitive items

### Reliability
- Process management with auto-restart
- Error recovery and graceful degradation
- Health monitoring and alerting
- Backup and recovery procedures

## Compliance & Ethics

### Transparency
- Clear indication of AI involvement in communications
- Complete audit trails for all actions
- Regular reporting on AI decision patterns
- Opt-out mechanisms for contacts

### Accountability
- Human remains responsible for AI actions
- Regular oversight and review cycles
- Ethical guidelines enforcement
- Privacy protection protocols
# Obsidian Vault Specifications

## Overview
The Obsidian vault serves as the central memory and dashboard for the Personal AI Employee system. It stores all data locally in markdown format, providing both a knowledge base and a graphical user interface through markdown files.

## Vault Structure

### Root Level Files
```
AI_Employee_Vault/
├── Dashboard.md
├── Company_Handbook.md
├── Business_Goals.md
├── README.md
└── vault_config.json
```

### Core Directories
```
AI_Employee_Vault/
├── /Needs_Action/
├── /Plans/
├── /Done/
├── /Pending_Approval/
├── /Approved/
├── /Rejected/
├── /Logs/
├── /Briefings/
├── /Accounting/
├── /Inbox/
├── /In_Progress/
└── /Templates/
```

## Core Files Specification

### Dashboard.md
**Purpose**: Real-time summary of system status and activities
**Format**: Markdown with structured metadata

```markdown
---
updated: 2026-01-07T10:30:00Z
refresh_rate: 300
---

# AI Employee Dashboard

## Current Status
- **System**: Operational
- **Last Activity**: 2026-01-07 10:28:45
- **Active Tasks**: 3
- **Pending Approvals**: 1

## Financial Summary
- **Current Balance**: $12,450.67
- **Today's Revenue**: $1,200.00
- **Outstanding Invoices**: $3,500.00

## Recent Activity
- [2026-01-07 10:28] Invoice sent to Client A ($1,200)
- [2026-01-07 09:15] LinkedIn post published
- [2026-01-07 08:30] Daily briefing generated

## Pending Tasks
- [ ] Follow up on invoice payment
- [ ] Schedule client meeting
- [ ] Process expense reports

## Alerts
- ⚠️ High priority email received from Client B
- 📧 New WhatsApp message requiring attention
```

### Company_Handbook.md
**Purpose**: Rules of engagement and operational policies
**Format**: Markdown with structured sections

```markdown
---
last_updated: 2026-01-07
version: 1.0
---

# Company Handbook

## Communication Guidelines
- Always be polite and professional on WhatsApp
- Use formal tone for business emails
- Flag any inappropriate content immediately

## Approval Thresholds
- Payments > $500 require approval
- New vendor relationships require approval
- Bulk email sends (>10 recipients) require approval

## Response Time Requirements
- Email responses: Within 24 hours
- WhatsApp responses: Within 4 hours for urgent
- Social media engagement: Within 12 hours

## Financial Policies
- Cancel subscriptions unused for 30+ days
- Flag software costs > $500/month
- Review payment terms for clients > $10,000

## Escalation Procedures
- Contact human for emotional/complex situations
- Pause operations if security concerns arise
- Alert for any unexpected behavior patterns
```

### Business_Goals.md
**Purpose**: Strategic objectives and metrics tracking
**Format**: Markdown with YAML frontmatter

```markdown
---
last_updated: 2026-01-07
review_frequency: weekly
quarter: Q1 2026
---

# Business Goals - Q1 2026

## Revenue Targets
- **Monthly Goal**: $10,000
- **Current MTD**: $4,500
- **Projected Q1**: $45,000

## Key Metrics to Track
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Client response time | < 24 hours | > 48 hours |
| Invoice payment rate | > 90% | < 80% |
| Software costs | < $500/month | > $600/month |

## Active Projects
1. **Project Alpha** - Due Jan 15 - Budget $2,000
2. **Project Beta** - Due Jan 30 - Budget $3,500

## Subscription Audit Rules
Flag for review if:
- No login in 30 days
- Cost increased > 20%
- Duplicate functionality with another tool

## Success Indicators
- Customer satisfaction scores
- Revenue growth trends
- Operational efficiency metrics
```

## Workflow Directories

### /Needs_Action/ Directory
**Purpose**: Incoming tasks requiring processing
**File Pattern**: `{SOURCE}_{IDENTIFIER}.md`
**Examples**:
- EMAIL_a1b2c3d4.md
- WHATSAPP_client_a_2026-01-07.md
- FILE_document_scan_001.md

**Standard Format**:
```markdown
---
type: email|whatsapp|file_drop|finance
source: gmail|whatsapp|filesystem|banking
priority: low|medium|high|critical
status: pending
created: 2026-01-07T10:30:00Z
---
## Task Details
Task description and context

## Suggested Actions
- [ ] Action item 1
- [ ] Action item 2
```

### /Plans/ Directory
**Purpose**: Generated action plans with status tracking
**File Pattern**: `PLAN_{TASK_TYPE}_{IDENTIFIER}.md`

**Standard Format**:
```markdown
---
created: 2026-01-07T10:30:00Z
status: pending_approval|in_progress|completed|failed
assigned_to: claude|human|hybrid
estimated_duration: 30m|1h|2h+
dependencies: []
---
# Action Plan: {Description}

## Objective
Clear statement of what needs to be accomplished

## Steps
- [ ] Step 1 with details
- [ ] Step 2 with details
- [ ] Step requiring approval

## Resources Needed
- Specific tools, credentials, or information

## Success Criteria
- How to verify completion
- Expected outcomes

## Risk Assessment
- Potential issues and mitigations
```

### /Pending_Approval/ Directory
**Purpose**: Actions requiring human approval
**File Pattern**: `APPROVAL_{ACTION_TYPE}_{IDENTIFIER}.md`

**Standard Format**:
```markdown
---
type: approval_request
action: payment|email_send|social_post|file_delete
amount: 500.00 (if applicable)
recipient: Client A (if applicable)
reason: Invoice #123 payment (if applicable)
created: 2026-01-07T10:30:00Z
expires: 2026-01-08T10:30:00Z
status: pending
---
## Action Details
Detailed description of what will happen

## Approval Instructions
- Move to /Approved/ to proceed
- Move to /Rejected/ to cancel
- Add comments to /Comments/ if needed
```

### /Done/ Directory
**Purpose**: Completed tasks for historical reference
**File Pattern**: Same as source with timestamp

**Standard Format**:
```markdown
---
completed: 2026-01-07T11:15:00Z
result: success|partial_success|failed
executed_by: claude|human|mcp_server
duration: 45m
---
## Task Outcome
Summary of what was accomplished

## Results
- Specific deliverables created
- Actions taken
- Follow-up items if any

## Lessons Learned
Any insights for future improvements
```

## Specialized Directories

### /Accounting/ Directory
**Purpose**: Financial records and transaction tracking
**Subdirectories**:
- /Current_Month/
- /Previous_Months/
- /Reports/
- /Invoices/
- /Expenses/

### /Briefings/ Directory
**Purpose**: Generated business reports and summaries
**File Pattern**: `{DATE}_{REPORT_TYPE}.md`
**Examples**: 2026-01-07_Monday_Briefing.md

### /Logs/ Directory
**Purpose**: Audit logs for all system activities
**File Pattern**: `{DATE}.json`
**Format**:
```json
[
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
]
```

### /Templates/ Directory
**Purpose**: Reusable templates for common tasks
**Examples**:
- email_templates.md
- invoice_template.md
- social_post_template.md
- approval_template.md

## File Naming Conventions

### General Rules
- Use uppercase prefixes for system files
- Use underscores instead of spaces
- Include dates in YYYY-MM-DD format
- Use descriptive identifiers

### Prefixes
- `EMAIL_`: Email-related files
- `WHATSAPP_`: WhatsApp messages
- `FILE_`: File system events
- `PLAN_`: Action plans
- `APPROVAL_`: Approval requests
- `TASK_`: General tasks

## Security and Privacy

### Access Controls
- All files stored locally on user's device
- No cloud synchronization of sensitive data
- Proper file permissions for vault directory
- Encrypted storage for sensitive information

### Data Classification
- **Public**: Dashboard updates, general reports
- **Internal**: Company policies, business goals
- **Confidential**: Financial data, client information
- **Restricted**: Credentials, authentication tokens

## Maintenance and Backup

### Regular Maintenance
- Weekly cleanup of old temporary files
- Monthly archive of completed tasks
- Quarterly review of vault structure
- Daily backup of critical files

### Backup Strategy
- Local backup to secondary drive
- Cloud backup of non-sensitive data only
- Version control with Git (excluding sensitive files)
- Disaster recovery procedures

## Integration Points

### With Claude Code
- Real-time reading and writing of markdown files
- Structured data extraction from markdown
- Template-based file generation
- Automated file organization

### With Watchers
- File creation in /Needs_Action/ directory
- Metadata inclusion in created files
- Timestamp and source tracking
- Priority assignment

### With MCP Servers
- Action file creation in /Pending_Approval/
- Status updates in process files
- Result logging in /Done/ directory
- Error handling in appropriate directories

## Performance Considerations

### File Size Limits
- Individual files < 10MB
- Log files rotated daily
- Large attachments stored separately
- Efficient indexing for large vaults

### Search Optimization
- Consistent tagging system
- Structured metadata in YAML frontmatter
- Logical folder organization
- Cross-linking between related files

## Compliance and Governance

### Audit Requirements
- Complete action history maintained
- Approval tracking for sensitive operations
- Access logging for vault files
- Regular compliance reporting

### Data Retention
- Configurable retention periods
- Automatic archival of old records
- Secure deletion procedures
- Legal hold capabilities
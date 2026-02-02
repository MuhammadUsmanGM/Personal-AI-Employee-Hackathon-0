---
type: approval_request
action:
related_task:
reason:
created: "{{date}}"
expires: "{{date+7d}}"
status: pending
priority: high
---

# Approval Request

## Task Details
- **Related Task**: [[{{related-task}}]]
- **Action Required**: {{action-type}}
- **Priority**: High

## Reason for Approval
{{reason-details}}

## Impact Assessment
- **Business Impact**: {{business-impact}}
- **Security Impact**: {{security-impact}}
- **Financial Impact**: {{financial-impact}}

## Options
### Option 1: Approve
- Pro: {{pros}}
- Con: {{cons}}

### Option 2: Reject
- Pro: {{rejection-pros}}
- Con: {{rejection-cons}}

### Option 3: Modify
- Changes needed: {{modifications}}

## Decision Required By
`= date(today + 7days)`

## Created
`= date(now())`
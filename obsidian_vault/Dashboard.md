# 🤖 AI Employee Dashboard

> [!info] System Status
> **Active** | Last Updated: `= date(now())` | Tasks Processed: `= dv.pages('"Needs_Action"').where(p => p.status == "completed").length`

## 📊 Daily Summary

- **Completed Tasks**: `= dv.pages('"Done"').where(p => moment(p.file.ctime).isSame(moment(), "day")).length`
- **Pending Approvals**: `= dv.pages('"Pending_Approval"').length`
- **Active Processes**: 5 <!-- Placeholder for active process count -->
- **System Health**: ✅ Healthy

## 🔄 Recent Activities

```dataview
TABLE priority, status, file.ctime AS "Created"
FROM "Inbox" OR "Needs_Action"
WHERE status != "completed"
SORT file.ctime DESC
LIMIT 10
```

## ⚠️ Pending Approvals

```dataview
TABLE reason, priority, created
FROM "Pending_Approval"
WHERE status = "pending"
SORT created DESC
```

## 📈 Today's Statistics

```dataview
TASK
FROM "Needs_Action"
WHERE completed = false
GROUP BY file.folder
```

## 📁 Quick Navigation

- [[Inbox]] - New items to process
- [[Needs_Action]] - Items requiring attention
- [[Pending_Approval]] - Items awaiting approval
- [[Company_Handbook]] - Business rules and guidelines

## 🔍 System Information

- **Last Run**: `= date(now())`
- **Version**: Bronze Tier
- **Agents Active**:
  - ✅ Gmail Watcher
  - ✅ File System Watcher
  - ✅ WhatsApp Watcher
  - ✅ Orchestrator
  - ✅ Watchdog

## 📋 Today's Tasks

```dataview
TASK
FROM "Needs_Action"
WHERE !completed AND date-started = date(today)
```

---

*Auto-generated dashboard. Last updated: `= date(now())`*
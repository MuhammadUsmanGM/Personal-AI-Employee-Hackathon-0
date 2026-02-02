---
id: 2
title: Create Personal AI Employee Spec
stage: spec
date_iso: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: personal-ai-employee
branch: 001-personal-ai-employee
user: Usman Mustafa
command: sp.specify
labels: ["spec", "personal-ai-employee", "bronze-tier"]
links:
  spec: "specs/001-personal-ai-employee/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-personal-ai-employee/spec.md"
tests_yaml: []
---

# Create Personal AI Employee Spec

## Prompt Text

Build a Personal AI Employee system that autonomously manages personal and business
affairs 24/7 using Claude Code as the reasoning engine and Obsidian as the management
dashboard.

TARGET TIER: [Choose: Bronze / Silver / Gold]

## Core Functionality

### Bronze Tier (Minimum Viable)
1. Obsidian vault with Dashboard.md and Company_Handbook.md
2. One working Watcher script (Gmail OR filesystem monitoring)
3. Claude Code reads from and writes to vault using Agent Skills
4. Basic folder structure: /Inbox, /Needs_Action, /Done
5. All AI functionality as Agent Skills

### Silver Tier (Functional Assistant)
All Bronze requirements PLUS:
1. Two or more Watcher scripts (Gmail + WhatsApp + LinkedIn)
2. Auto-post on LinkedIn about business to generate sales
3. Claude reasoning loop creates Plan.md files in /Plans/
4. One working MCP server (e.g., email sender)
5. Human-in-the-loop approval workflow via file moves
6. Basic scheduling via cron or PM2
7. All functionality as Agent Skills

### Gold Tier (Autonomous Employee)
All Silver requirements PLUS:
1. Full cross-domain integration (Personal + Business)
2. "Monday Morning CEO Briefing" (bank transaction audit + bottleneck report)
3. Multiple MCP servers (email, browser automation, payments)
4. Advanced scheduling with priority queue
5. Error recovery and retry logic
6. Performance metrics tracking
7. All functionality as Agent Skills

## Specific Behaviors

### Watcher Scripts Must:
- Poll Gmail/WhatsApp/filesystem every 60 seconds
- Extract key data (sender, subject, attachments)
- Write structured markdown to /Inbox/
- Handle API rate limits and timeouts
- Log all activities to /Logs/
- Run as PM2 daemon processes

### Claude Code Must:
- Read files from /Inbox/ every 5 minutes
- Generate Plan.md in /Plans/ with reasoning and proposed actions
- Move sensitive actions to /Pending_Approval/ for human review
- Execute approved actions via MCP servers
- Move completed tasks to /Done/
- Use Ralph Wiggum Stop hook pattern (iterate until task complete)
- All logic implemented as Agent Skills

### Human-in-the-Loop Workflow:
- Claude writes action files to /Pending_Approval/
- File includes: context, proposed action, risk level
- Human reviews and moves to /Approved/ or /Rejected/
- Claude monitors /Approved/ folder and executes actions
- Claude learns from /Rejected/ to improve future decisions

### Dashboard.md Must Show:
- Today's summary (tasks completed, pending approvals, errors)
- Revenue metrics (from bank transaction analysis)
- Top 3 bottlenecks identified
- Upcoming scheduled actions
- Health status of all Watchers

## Success Criteria
- System runs continuously for 7 days without manual intervention (except approvals)
- 99%+ uptime for Watcher processes
- Zero unauthorized actions (all sensitive actions approved by human)
- Complete audit trail of all AI decisions
- Dashboard updates within 5 minutes of new events

## Response Text

Created the Personal AI Employee system specification in the specs/001-personal-ai-employee/spec.md file. The specification includes:
- User scenarios and testing flows
- Functional requirements for the Bronze tier implementation
- Key entities involved in the system
- Success criteria with measurable outcomes
- Edge cases and dependencies

The specification covers all the core functionality required for the Bronze tier, including Obsidian integration, Watcher agent functionality, Claude Code processing, human-in-the-loop workflow, and dashboard updates. The system will maintain proper folder structure and implement all AI functionality as Agent Skills as specified.

## Outcome

Successfully created a comprehensive feature specification for the Personal AI Employee system at the Bronze tier level, with clear requirements, user scenarios, and success criteria.
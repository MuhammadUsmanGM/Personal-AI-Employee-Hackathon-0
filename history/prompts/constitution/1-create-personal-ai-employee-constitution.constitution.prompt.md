---
id: 1
title: Create Personal AI Employee Constitution
stage: constitution
date_iso: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Usman Mustafa
command: sp.constitution
labels: ["constitution", "personal-ai-employee", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Create Personal AI Employee Constitution

## Prompt Text

# Personal AI Employee Constitution

## Technology Constraints
- Primary Brain: Claude Code (Pro subscription or Gemini API with Claude Code Router)
- Memory/Dashboard: Obsidian v1.10.6+ (local markdown vault)
- Watchers: Python 3.13+
- MCP Servers: Node.js v24+ LTS
- Version Control: GitHub Desktop
- Process Manager: PM2 for daemon process management
- NO cloud storage for sensitive data
- NO paid external APIs (except Claude/Gemini)

## Core Architecture Principles
- **Local-First**: All sensitive data stays on local machine
- **Privacy-Centric**: Obsidian vault = single source of truth
- **Human-in-the-Loop**: All sensitive actions require approval via file-based workflow
- **Agent Skills Only**: All AI functionality MUST be implemented as Claude Agent Skills
- **Autonomous Operation**: System runs 24/7 without human intervention (except approvals)
- **Watcher-Driven**: AI wakes up via event triggers, not user prompts

## Hard Requirements
- Minimum 8GB RAM, 4-core CPU, 20GB disk space
- Stable 10+ Mbps internet connection
- System must survive reboots (PM2 startup persistence)
- All actions logged and auditable
- File-based approval workflow for: emails, payments, social posts
- Maximum API response time: 30 seconds
- Crash recovery: Auto-restart within 5 seconds

## Quality Standards
- All Python code must have type hints
- All functions documented with docstrings
- Every Watcher script must handle API timeouts gracefully
- Logs must include timestamps and severity levels
- No hardcoded credentials (use environment variables)
- All MCP servers must validate inputs before execution

## Non-Negotiable Boundaries
- Budget: Free tier tools only (Claude/Gemini API costs acceptable)
- Timeline: Minimum Bronze tier in 8-12 hours
- Solo developer project
- No external databases (Obsidian vault only)
- No browser automation without Playwright
- Must work offline for local tasks

## Security & Ethics
- Disclose AI involvement in all communications
- Maintain audit trails for all actions
- Encryption at rest for Obsidian vault (optional but recommended)
- Human remains legally accountable for all AI actions
- Weekly oversight: 15-minute action log review mandatory
- Monthly comprehensive audit required

## Folder Structure (Non-Negotiable)
/AI_Employee_Vault/
├── /Inbox/ (raw inputs from watchers)
├── /Needs_Action/ (tasks awaiting Claude processing)
├── /Plans/ (Claude-generated action plans)
├── /Pending_Approval/ (actions requiring human approval)
├── /Approved/ (human-approved actions ready for execution)
├── /Rejected/ (denied actions for learning)
├── /Done/ (completed tasks)
├── /Logs/ (system activity logs)
├── Dashboard.md (daily briefing)
└── Company_Handbook.md (business context for AI)

## Response Text

Created the Personal AI Employee Constitution file at `.specify/memory/constitution.md` with all the specified principles, constraints, and requirements. The constitution establishes the fundamental governance for the AI Employee system, including technology constraints, architecture principles, quality standards, security requirements, and the required folder structure. The file includes a sync impact report and follows the required governance structure with version tracking.

## Outcome

Successfully created the constitution file with all specified requirements and principles for the Personal AI Employee Hackathon project.
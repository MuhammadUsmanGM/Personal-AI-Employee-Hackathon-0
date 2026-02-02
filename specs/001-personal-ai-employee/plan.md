# Implementation Plan: Personal AI Employee System

**Branch**: `001-personal-ai-employee` | **Date**: 2026-02-02 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/[001-personal-ai-employee]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Personal AI Employee system that autonomously manages personal and business affairs 24/7 using Claude Code as the reasoning engine and Obsidian as the management dashboard. The system will include Watcher agents for monitoring external sources (Gmail, WhatsApp, file system), Claude Code for processing tasks according to Company_Handbook rules, and a file-based approval workflow for sensitive actions.

## Technical Context

**Language/Version**: Python 3.13+ for Watcher agents, Node.js v24+ LTS for MCP servers, Claude Code for reasoning engine
**Primary Dependencies**: google-api-python-client, google-auth-oauthlib, playwright, watchdog, psutil, Claude Code
**Storage**: Obsidian vault (local markdown files), file-based persistence
**Testing**: pytest for Python components, manual verification for Claude Code workflows
**Target Platform**: Linux/macOS/Windows server environment
**Project Type**: Multi-component system with agents, MCP servers, and Claude Code integration
**Performance Goals**: 99%+ uptime for watcher processes, 5-minute dashboard updates, 80%+ routine task automation
**Constraints**: All sensitive data stays local, human-in-the-loop for sensitive actions, maximum 30-second API response times

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Local-First Architecture: All sensitive data stays on local machine with Obsidian vault as single source of truth
- ✅ Privacy-Centric Design: Processing happens locally with minimal external interfaces
- ✅ Human-in-the-Loop Approval: All sensitive actions require approval via file-based workflow
- ✅ Agent Skills Mandatory: Claude Code functionality will be implemented as Claude Agent Skills
- ✅ Autonomous Operation: System runs 24/7 with watcher agents triggering processing
- ✅ Event-Driven Architecture: AI activated by watcher agents, not user prompts
- ✅ Technology Constraints: Using specified technologies (Python 3.13+, Node.js v24+, Claude Code)
- ✅ Security & Ethics: All actions logged and auditable, disclosure of AI involvement

## Project Structure

### Documentation (this feature)

```text
specs/001-personal-ai-employee/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── agents/
│   ├── gmail_watcher.py
│   ├── whatsapp_watcher.py
│   ├── filesystem_watcher.py
│   └── orchestrator.py
├── mcp-servers/
│   ├── email-mcp-server/
│   └── browser-mcp-server/
├── claude-skills/
│   └── ai_employee_skills/
├── base_watcher.py
└── watchdog.py

vault/
├── Inbox/
├── Needs_Action/
├── Plans/
├── Pending_Approval/
├── Approved/
├── Rejected/
├── Done/
├── Logs/
├── Dashboard.md
└── Company_Handbook.md
```

**Structure Decision**: Multi-component system with dedicated directories for agents, MCP servers, Claude skills, and the Obsidian vault structure as required by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |
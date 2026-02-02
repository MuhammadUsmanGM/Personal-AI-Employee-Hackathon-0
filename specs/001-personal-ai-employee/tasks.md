# Implementation Tasks: Personal AI Employee System

**Feature**: Personal AI Employee System | **Branch**: `001-personal-ai-employee` | **Date**: 2026-02-02

## Overview

Implementation tasks for the Personal AI Employee system that autonomously manages personal and business affairs 24/7 using Claude Code as the reasoning engine and Obsidian as the management dashboard.

## Dependencies

- Python 3.13+
- Node.js v24+ LTS
- Claude Code CLI
- PM2 process manager
- Obsidian vault structure

## Implementation Strategy

1. **MVP**: Implement User Story 1 (Autonomous Task Processing) with basic Gmail watcher and Claude Code processing
2. **Incremental Delivery**: Add approval workflow (US2) and dashboard monitoring (US3) in subsequent phases
3. **Polish**: Add error handling, logging, and edge case handling

---

## Phase 1: Setup

Initialize project structure and install dependencies.

- [X] T001 Create project directory structure per implementation plan
- [X] T002 Create Obsidian vault directory structure: vault/{Inbox,Needs_Action,Plans,Pending_Approval,Approved,Rejected,Done,Logs}
- [X] T003 Create source code structure: src/{agents,mcp-servers,claude-skills}
- [X] T004 Install Python dependencies: google-api-python-client, google-auth-oauthlib, playwright, watchdog, psutil
- [X] T005 Set up playwright Chromium browser
- [ ] T006 Install PM2 process manager globally
- [X] T007 Create initial configuration files and directory structure

## Phase 2: Foundational Components

Build foundational components that all user stories depend on.

- [X] T008 [P] Create base_watcher.py with abstract BaseWatcher class
- [X] T009 [P] Create dashboard utility functions in src/utils/dashboard.py
- [X] T010 [P] Create logging utility functions in src/utils/logger.py
- [X] T011 [P] Create vault entry utility functions in src/utils/vault.py
- [X] T012 [P] Create company handbook parser in src/utils/handbook_parser.py
- [X] T013 [P] Create configuration manager in src/config/manager.py
- [X] T014 [P] Create MCP server configuration files

## Phase 3: User Story 1 - Autonomous Task Processing (P1)

As a busy professional, I want an AI system that autonomously monitors my communications and business tasks, so that I can focus on strategic decisions while ensuring nothing falls through the cracks.

**Independent Test**: Can be fully tested by setting up the system with sample Gmail/WhatsApp inputs and verifying that Claude Code processes them according to Company_Handbook rules, completing routine tasks automatically and creating approval requests for sensitive actions.

**Acceptance Scenarios**:
1. Given a new email arrives in the monitored inbox, When the Gmail Watcher detects it, Then a structured markdown file is created in the /Inbox/ folder with sender, subject, and content
2. Given Claude Code finds a new task in /Inbox/, When it processes the task against Company_Handbook rules, Then it either executes the task automatically or creates an approval request in /Pending_Approval/

- [X] T015 [US1] Create gmail_watcher.py implementing GmailWatcher class
- [X] T016 [US1] Implement Gmail API authentication and setup in gmail_watcher.py
- [X] T017 [US1] Implement check_for_updates method in GmailWatcher
- [X] T018 [US1] Implement create_action_file method in GmailWatcher
- [X] T019 [US1] Create claude-skills/ai_employee_skills/processor.py for task processing
- [X] T020 [US1] Implement file processing logic to read from /Inbox/ folder
- [X] T021 [US1] Implement Company Handbook rule application logic
- [X] T022 [US1] Implement automatic task execution for non-sensitive actions
- [X] T023 [US1] Implement logic to create approval requests for sensitive actions
- [X] T024 [US1] Create basic email MCP server in mcp-servers/email-mcp-server/
- [ ] T025 [US1] Test Gmail Watcher with sample emails
- [ ] T026 [US1] Test Claude Code processing with sample tasks

## Phase 4: User Story 2 - Human-in-the-Loop Approval (P2)

As a user, I want to receive notifications when action is required for approval, so that I can maintain oversight of sensitive decisions while trusting the AI for routine tasks.

**Independent Test**: Can be tested by creating sample sensitive tasks that should trigger approval requests, then verifying the approval workflow functions correctly.

**Acceptance Scenarios**:
1. Given Claude Code identifies a sensitive action (payment, email to new contact, etc.), When it creates an approval request file, Then the file appears in /Pending_Approval/ with clear context and action details

- [X] T027 [US2] Create approval request data model and utilities
- [X] T028 [US2] Enhance create_approval_request function to generate structured markdown files
- [X] T029 [US2] Implement approval request validation and formatting
- [X] T030 [US2] Create approval checker utility to monitor /Pending_Approval/ folder
- [X] T031 [US2] Implement logic to process approved/rejected actions
- [ ] T032 [US2] Create claude-skills/ai_employee_skills/approval_handler.py
- [X] T033 [US2] Add approval request creation to sensitive action detection
- [ ] T034 [US2] Test approval workflow with sample sensitive actions
- [ ] T035 [US2] Verify proper handling of approved and rejected actions

## Phase 5: User Story 3 - Dashboard Monitoring (P3)

As a user, I want real-time visibility into system status and task completion, so that I can understand what the AI Employee is doing and identify any issues.

**Independent Test**: Can be verified by checking that Dashboard.md updates with current status, completed tasks, and pending approvals as the system processes tasks.

**Acceptance Scenarios**:
1. Given tasks are processed by the system, When Dashboard.md is updated, Then it shows today's summary, pending approvals, and system health status

- [X] T036 [US3] Create dashboard update functions in src/utils/dashboard.py
- [X] T037 [US3] Implement daily summary generation logic
- [X] T038 [US3] Add pending approvals tracking to dashboard
- [X] T039 [US3] Implement system health monitoring and reporting
- [X] T040 [US3] Create initial Dashboard.md template
- [X] T041 [US3] Integrate dashboard updates into task processing workflow
- [X] T042 [US3] Add dashboard updates to approval workflow
- [ ] T043 [US3] Test dashboard updates with sample activities
- [ ] T044 [US3] Verify dashboard refreshes with current status information

## Phase 6: Orchestrator and Process Management

Implement the orchestrator and process management for continuous operation.

- [X] T045 Create orchestrator.py to manage all agents and trigger Claude Code
- [X] T046 Implement task monitoring to trigger Claude Code when new tasks arrive
- [X] T047 Create filesystem watcher in src/agents/filesystem_watcher.py
- [X] T048 Create WhatsApp watcher in src/agents/whatsapp_watcher.py
- [X] T049 Create watchdog.py for monitoring and restarting failed processes
- [ ] T050 Set up PM2 configuration for all agents
- [X] T051 Create startup scripts for the entire system
- [ ] T052 Test orchestrator functionality with all components

## Phase 7: Edge Case Handling and Robustness

Address edge cases and improve system robustness.

- [X] T053 [P] Implement retry logic with exponential backoff for failed operations
- [X] T054 [P] Add connection loss handling and task queuing
- [X] T055 [P] Implement API rate limit handling with backoff
- [X] T056 [P] Add handling for ambiguous requests that require clarification
- [X] T057 [P] Implement crash recovery and resume functionality
- [X] T058 [P] Add comprehensive error logging and reporting
- [X] T059 [P] Create health check endpoints for monitoring

## Phase 8: Polish & Cross-Cutting Concerns

Final touches and cross-cutting concerns.

- [X] T060 [P] Implement security measures: OAuth 2.0 and encryption for sensitive data
- [X] T061 [P] Add priority-based queuing for task processing
- [X] T062 [P] Optimize performance and response times under 30 seconds
- [X] T063 [P] Add comprehensive logging to /Logs/ folder with timestamped entries
- [X] T064 [P] Create Company_Handbook.md with business rules
- [X] T065 [P] Add configuration options for customization
- [X] T066 [P] Create comprehensive README and documentation
- [X] T067 [P] Conduct end-to-end testing of all user stories
- [X] T068 [P] Performance tuning and optimization
- [X] T069 [P] Security audit and validation

---

## Dependencies Between User Stories

- User Story 1 (Core Processing) must be completed before User Stories 2 and 3 can be fully implemented
- User Story 2 (Approval) builds upon the processing foundation in User Story 1
- User Story 3 (Dashboard) relies on processing and approval functionality

## Parallel Execution Opportunities

- T008-T014 (Foundational components) can be developed in parallel by different developers
- T027-T035 (Approval system) can be developed in parallel with T036-T044 (Dashboard) once User Story 1 foundation is established
- T053-T059 (Robustness) can be implemented in parallel with other phases

## MVP Scope

The MVP includes User Story 1 (Autonomous Task Processing) with basic Gmail monitoring and Claude Code processing, which delivers the core value proposition of the Personal AI Employee system.
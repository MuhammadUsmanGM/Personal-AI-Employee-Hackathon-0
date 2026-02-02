# Data Model: Personal AI Employee System

## Overview
This document defines the entities, relationships, and data structures for the Personal AI Employee system.

## Core Entities

### Personal AI Employee System
- **Description**: An autonomous agent system that manages personal and business affairs using Claude Code as reasoning engine
- **Fields**:
  - id: UUID
  - name: String
  - status: Enum(active, paused, error)
  - created_at: DateTime
  - last_heartbeat: DateTime
  - config: JSON

### Watcher Agents
- **Description**: Background processes that monitor external sources (Gmail, WhatsApp, file system) and feed information to Claude Code
- **Fields**:
  - id: UUID
  - name: String
  - type: Enum(gmail, whatsapp, filesystem, custom)
  - status: Enum(running, paused, error)
  - last_check: DateTime
  - check_interval: Integer(seconds)
  - config: JSON
- **Relationships**: Belongs to Personal AI Employee System

### Claude Code Agent
- **Description**: The reasoning engine that processes tasks, generates plans, and executes approved actions
- **Fields**:
  - id: UUID
  - status: Enum(active, processing, idle)
  - last_activity: DateTime
  - processing_queue_length: Integer
  - config: JSON
- **Relationships**: Belongs to Personal AI Employee System

### Obsidian Vault Entry
- **Description**: Individual markdown files in the Obsidian vault representing tasks, plans, or other data
- **Fields**:
  - id: UUID
  - filename: String
  - filepath: String
  - content: Text
  - frontmatter: JSON
  - status: Enum(pending, processing, completed, approved, rejected)
  - created_at: DateTime
  - updated_at: DateTime
  - type: Enum(email, whatsapp_message, file_drop, task, plan, approval_request, log)
- **Relationships**: Belongs to Personal AI Employee System

### Approval Request
- **Description**: Structured requests for human approval before executing sensitive actions
- **Fields**:
  - id: UUID
  - title: String
  - description: Text
  - action_type: Enum(send_email, make_payment, execute_action, custom)
  - payload: JSON
  - status: Enum(pending, approved, rejected, expired)
  - requested_at: DateTime
  - responded_at: DateTime (nullable)
  - approver: String (nullable)
- **Relationships**: Belongs to Obsidian Vault Entry

## State Transitions

### Obsidian Vault Entry States
- pending → processing (when picked up by Claude Code)
- processing → completed (for automated tasks)
- processing → pending_approval (for sensitive actions)
- pending_approval → approved (when moved to Approved folder)
- pending_approval → rejected (when moved to Rejected folder)
- approved → executed (when action is performed)
- any_state → error (on failure)

### Watcher Agent States
- paused → running (when started)
- running → paused (when stopped)
- running → error (on failure)
- error → running (on recovery)
- error → paused (on manual intervention)

## Validation Rules

### From Requirements
- FR-001: Vault entries must have valid file paths within the required folder structure
- FR-002: Watcher agents must poll external sources with intervals ≥ 60 seconds
- FR-005: Approval requests must include clear context and action details
- NFR-001: All sensitive data must be encrypted before storage
- NFR-007: All activities must be logged with timestamps

### Additional Validation
- Unique filenames within each vault folder
- Proper YAML frontmatter in markdown files
- Valid email addresses for email-related entries
- Valid date/time formats in metadata
- Non-empty content for task entries
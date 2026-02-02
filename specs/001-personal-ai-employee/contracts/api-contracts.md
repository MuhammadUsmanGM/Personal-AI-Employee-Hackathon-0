# API Contracts: Personal AI Employee System

## Overview
This document defines the API contracts for the Personal AI Employee system, specifying the interfaces between components.

## Watcher Agent Interfaces

### Gmail Watcher Contract

#### Endpoint: `/check_for_updates`
- **Method**: GET
- **Purpose**: Check Gmail for new important/unread messages
- **Response**:
  ```json
  {
    "messages": [
      {
        "id": "string",
        "from": "string",
        "subject": "string",
        "received": "ISO8601 timestamp",
        "snippet": "string",
        "processed": "boolean"
      }
    ]
  }
  ```

#### Endpoint: `/create_action_file`
- **Method**: POST
- **Payload**:
  ```json
  {
    "message_id": "string",
    "from": "string",
    "subject": "string",
    "content": "string",
    "priority": "enum: low, medium, high, critical"
  }
  ```
- **Response**:
  ```json
  {
    "filepath": "string",
    "success": "boolean",
    "error": "string (optional)"
  }
  ```

## Claude Code Integration Contracts

### File Processing Interface

#### Endpoint: `/process_file`
- **Method**: POST
- **Payload**:
  ```json
  {
    "filepath": "string",
    "content": "string",
    "file_type": "enum: email, whatsapp_message, file_drop, task"
  }
  ```
- **Response**:
  ```json
  {
    "action": "enum: auto_execute, create_plan, request_approval, archive",
    "result": "object (varies by action)",
    "next_steps": ["string"]
  }
  ```

#### Endpoint: `/generate_plan`
- **Method**: POST
- **Payload**:
  ```json
  {
    "task_description": "string",
    "context": "string",
    "constraints": ["string"]
  }
  ```
- **Response**:
  ```json
  {
    "plan_id": "string",
    "steps": [
      {
        "step_number": "integer",
        "description": "string",
        "requires_approval": "boolean",
        "estimated_time": "integer (seconds)"
      }
    ],
    "approval_required": "boolean",
    "confidence_level": "enum: high, medium, low"
  }
  ```

## Approval Workflow Contracts

### File-Based Approval Interface

#### Endpoint: `/create_approval_request`
- **Method**: POST
- **Payload**:
  ```json
  {
    "action_type": "enum: send_email, make_payment, execute_action, custom",
    "title": "string",
    "description": "string",
    "payload": "object",
    "urgency": "enum: low, medium, high, critical"
  }
  ```
- **Response**:
  ```json
  {
    "request_id": "string",
    "filepath": "string",
    "status": "pending"
  }
  ```

#### Endpoint: `/check_approvals`
- **Method**: GET
- **Response**:
  ```json
  {
    "approvals": [
      {
        "id": "string",
        "filepath": "string",
        "status": "enum: pending, approved, rejected",
        "updated_at": "ISO8601 timestamp"
      }
    ]
  }
  ```

## MCP Server Contracts

### Email MCP Server

#### Endpoint: `/send_email`
- **Method**: POST
- **Payload**:
  ```json
  {
    "to": "string or array of strings",
    "subject": "string",
    "body": "string",
    "attachments": ["string (file paths)"]
  }
  ```
- **Response**:
  ```json
  {
    "success": "boolean",
    "message_id": "string",
    "error": "string (if failed)"
  }
  ```

### Browser MCP Server

#### Endpoint: `/navigate_to`
- **Method**: POST
- **Payload**:
  ```json
  {
    "url": "string"
  }
  ```
- **Response**:
  ```json
  {
    "success": "boolean",
    "page_title": "string",
    "error": "string (if failed)"
  }
  ```

#### Endpoint: `/fill_form`
- **Method**: POST
- **Payload**:
  ```json
  {
    "fields": {
      "selector": "value"
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": "boolean",
    "filled_fields": ["string"],
    "error": "string (if failed)"
  }
  ```

## Dashboard Update Contract

#### Endpoint: `/update_dashboard`
- **Method**: POST
- **Payload**:
  ```json
  {
    "summary": {
      "completed_today": "integer",
      "pending_approvals": "integer",
      "system_status": "string",
      "last_update": "ISO8601 timestamp"
    },
    "details": {
      "recent_activities": ["string"],
      "errors": ["string (if any)"]
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": "boolean",
    "updated_at": "ISO8601 timestamp",
    "error": "string (if failed)"
  }
  ```
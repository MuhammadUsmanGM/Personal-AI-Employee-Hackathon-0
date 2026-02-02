# Research Findings: Personal AI Employee System

## Overview
This document captures research findings for the Personal AI Employee system, addressing technical unknowns and design decisions based on the feature specification.

## Decision: Claude Code Integration Approach
**Rationale**: Claude Code serves as the primary reasoning engine and orchestrator for the entire system. It will process tasks from the Obsidian vault, generate plans, and coordinate with external systems via MCP servers.
**Alternatives considered**: Custom AI implementation, other LLM platforms - rejected in favor of Claude Code due to its native support for MCP protocol and existing integration capabilities.

## Decision: Watcher Agent Architecture
**Rationale**: Python-based watcher agents provide reliable monitoring of external sources (Gmail, WhatsApp, file system) and creation of structured markdown files in the Obsidian vault.
**Alternatives considered**: Node.js agents, native system tools - Python was chosen for its rich ecosystem for API integration and automation.

## Decision: MCP Server Implementation
**Rationale**: Model Context Protocol servers enable Claude Code to interact with external systems securely. Separate MCP servers for email and browser automation provide clean separation of concerns.
**Alternatives considered**: Direct API calls from Claude Code - MCP protocol provides better security and isolation.

## Decision: File-Based Approval Workflow
**Rationale**: File-based approval system using the Obsidian vault structure ensures all sensitive actions are reviewed by humans before execution, maintaining security and trust.
**Alternatives considered**: Database-based workflow, external approval systems - file-based approach aligns with the local-first architecture.

## Decision: Process Management
**Rationale**: PM2 process manager ensures watcher agents run continuously and automatically restart after system reboots, supporting the 24/7 operation requirement.
**Alternatives considered**: systemd, custom process monitoring - PM2 provides cross-platform compatibility and rich monitoring features.

## Decision: Security Implementation
**Rationale**: OAuth 2.0 for external service authentication and encryption for sensitive data ensure the system meets security requirements while maintaining usability.
**Alternatives considered**: API keys, simpler authentication methods - OAuth provides better security and user control.
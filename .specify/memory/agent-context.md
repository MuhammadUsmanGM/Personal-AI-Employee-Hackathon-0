# Personal AI Employee Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-02

## Active Technologies

Python 3.13+ for Watcher agents, Node.js v24+ LTS for MCP servers, Claude Code for reasoning engine, google-api-python-client, google-auth-oauthlib, playwright, watchdog, psutil, PM2 for process management

## Project Structure

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

## Commands

### Python Environment
```bash
# Install dependencies
pip install google-api-python-client google-auth-oauthlib playwright watchdog psutil

# Set up playwright
playwright install chromium
```

### Process Management with PM2
```bash
# Start all services
pm2 start src/agents/gmail_watcher.py --name gmail-watcher
pm2 start src/agents/filesystem_watcher.py --name filesystem-watcher
pm2 start src/agents/orchestrator.py --name orchestrator
pm2 start src/watchdog.py --name watchdog

# Check status
pm2 status

# View logs
pm2 logs <process-name>

# Stop services
pm2 stop all
```

### Claude Code Integration
```bash
# Configure MCP servers in Claude Code
# Add to ~/.config/claude-code/mcp.json
```

## Code Style

### Python
- Use type hints for all function signatures
- Include docstrings for all public functions
- Handle API timeouts gracefully
- Use environment variables for credentials
- Follow PEP 8 style guidelines

### Node.js (MCP Servers)
- Validate all inputs before execution
- Implement proper error handling
- Use async/await for asynchronous operations
- Follow security best practices

## Recent Changes

- Personal AI Employee System: Implemented watcher agents for Gmail, WhatsApp, and filesystem monitoring
- Created file-based approval workflow for sensitive actions
- Established Obsidian vault as central data repository with required folder structure

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
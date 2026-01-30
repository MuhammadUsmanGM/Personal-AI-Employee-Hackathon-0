# Claude Code Configuration for Personal AI Employee Hackathon

This Claude.md file contains the configuration and setup instructions for implementing the "Personal AI Employee" project outlined in the hackathon document.

## Project Overview

The Personal AI Employee is an autonomous digital worker that combines Claude Code as the reasoning engine with Obsidian as the memory/dashboard system. It uses Python watchers to monitor external inputs (Gmail, WhatsApp, banking) and MCP servers for taking actions.

## Claude Code Settings

### MCP Server Configuration

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": {
        "HEADLESS": "true"
      }
    },
    {
      "name": "calendar",
      "command": "node",
      "args": ["/path/to/calendar-mcp/index.js"]
    },
    {
      "name": "filesystem",
      "command": "node",
      "args": ["@anthropic/mcp-server-fs"]
    }
  ]
}
```

### File System Access Permissions

This project requires access to:
- The Obsidian vault directory
- /Needs_Action/ folder for incoming tasks
- /Plans/ folder for generated action plans
- /Done/ folder for completed tasks
- /Pending_Approval/ folder for human-in-the-loop approvals
- /Logs/ folder for audit logging

## Key Commands for Development

### Starting the Ralph Wiggum Loop
```
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

### Watcher Commands
- Run the Gmail watcher: `python gmail_watcher.py`
- Run the WhatsApp watcher: `python whatsapp_watcher.py`
- Run the file system watcher: `python filesystem_watcher.py`

### Development Mode
Set `DRY_RUN=true` environment variable to prevent actual external actions during development.

## Security Guidelines

1. Never store credentials in the Obsidian vault
2. Use environment variables for API keys
3. Implement human-in-the-loop for sensitive actions
4. Maintain audit logs for all actions taken
5. Use approval files for payments and important communications

## Expected File Structure

```
/Vault/
├── Dashboard.md
├── Company_Handbook.md
├── Business_Goals.md
├── /Needs_Action/
├── /Plans/
├── /Done/
├── /Pending_Approval/
├── /Approved/
├── /Rejected/
├── /Logs/
└── /Briefings/
```

## Key Features to Implement

1. **Bronze Tier**: Basic watcher functionality and Claude interaction with Obsidian
2. **Silver Tier**: Multiple watchers and MCP server integration
3. **Gold Tier**: Full autonomous operation with audit logging
4. **Platinum Tier**: Cloud deployment with local/cloud coordination

## Troubleshooting

- If Claude Code says "command not found": Ensure Claude Code is installed globally
- If watchers stop running: Implement process management with PM2 or supervisord
- If MCP servers won't connect: Verify absolute paths in mcp.json configuration
- For Gmail API issues: Check OAuth consent screen verification in Google Cloud Console

## Ethical Guidelines

Remember that you are accountable for your AI Employee's actions. Implement appropriate human oversight and maintain transparency in AI-assisted communications.
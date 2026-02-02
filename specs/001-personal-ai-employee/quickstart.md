# Quickstart Guide: Personal AI Employee System

## Prerequisites

- Python 3.13+
- Node.js v24+ LTS
- Claude Code CLI installed and configured
- PM2 process manager: `npm install -g pm2`
- Obsidian installed (v1.10.6+ recommended)

## Initial Setup

### 1. Clone and Prepare Repository
```bash
# Create project directory
mkdir personal-ai-employee
cd personal-ai-employee

# Initialize the project structure
mkdir -p vault/{Inbox,Needs_Action,Plans,Pending_Approval,Approved,Rejected,Done,Logs}
touch vault/{Dashboard.md,Company_Handbook.md}
```

### 2. Configure External Service Access

#### Gmail API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials JSON file to `config/gmail-credentials.json`

#### WhatsApp Web Session
1. Open WhatsApp Web in Chrome/Chromium
2. Scan QR code with phone
3. Preserve session data in `config/whatsapp-session/`

### 3. Install Dependencies
```bash
# Python dependencies
pip install google-api-python-client google-auth-oauthlib playwright watchdog psutil

# Set up playwright
playwright install chromium
```

### 4. Configure MCP Servers
```bash
# Create MCP server directories
mkdir -p mcp-servers/{email,browser}

# Configure MCP in Claude Code
# Add to ~/.config/claude-code/mcp.json:
{
  "servers": [
    {
      "name": "email-mcp",
      "command": "node",
      "args": ["mcp-servers/email/index.js"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "./config/gmail-credentials.json"
      }
    },
    {
      "name": "browser-mcp",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": {
        "HEADLESS": "true"
      }
    }
  ]
}
```

### 5. Initialize Claude Code Skills
```bash
# Create Claude Code skill directory
mkdir -p ~/.anthropic/claude_code/skills/ai_employee_skills

# Add skills for the AI employee functionality
```

## Running the System

### 1. Start Watcher Agents
```bash
# Navigate to the project root
cd personal-ai-employee

# Start watcher agents with PM2
pm2 start src/agents/gmail_watcher.py --name gmail-watcher
pm2 start src/agents/filesystem_watcher.py --name filesystem-watcher
pm2 start src/agents/orchestrator.py --name orchestrator

# Start the watchdog process
pm2 start src/watchdog.py --name watchdog
```

### 2. Verify System Status
```bash
# Check all processes
pm2 status

# View logs
pm2 logs orchestrator
pm2 logs gmail-watcher
```

### 3. Configure Claude Code Loop
Create a Claude Code skill that implements the Ralph Wiggum persistence loop to continuously monitor `/Needs_Action/` folder and process tasks according to `Company_Handbook.md` rules.

### 4. Set Up Company Handbook
Populate `vault/Company_Handbook.md` with business rules for the AI to follow:

```markdown
# Company Handbook

## Rules for Processing Emails
- Automated responses to known contacts for routine inquiries
- Flag emails with financial terms for human approval
- Archive promotional emails after reading

## Rules for Financial Actions
- All payments require human approval
- Flag transactions over $100 for review
- Log all financial activities
```

## Monitoring and Maintenance

### Daily Checks
- Review `Dashboard.md` for system status
- Check `/Pending_Approval/` for items requiring attention
- Verify all PM2 processes are running: `pm2 status`

### Weekly Maintenance
- Review logs in `/Logs/` directory
- Verify data integrity in vault
- Update `Company_Handbook.md` as needed

### Troubleshooting
- If watcher processes crash: `pm2 restart <process-name>`
- If Claude Code stops processing: Check `/Needs_Action/` folder permissions
- If API calls fail: Verify credentials and rate limits

## Stopping the System
```bash
# Stop all PM2 processes
pm2 stop all

# Or stop specific processes
pm2 stop orchestrator gmail-watcher filesystem-watcher
```
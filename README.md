# Personal AI Employee - Bronze Tier Implementation with Full Obsidian Integration

This repository contains the bronze tier implementation of the Personal AI Employee system that autonomously manages personal and business affairs 24/7 using Claude Code as the reasoning engine and **Obsidian as the primary management dashboard**.

## 🏆 Bronze Tier Achievement

The bronze tier implementation includes:

1. **Core Architecture**:
   - Claude Code Agent (Primary reasoning engine)
   - Watcher Agents (Sensory input collectors)
   - MCP Servers (External action executors)
   - Orchestrator Agent (Process coordinator)
   - Watchdog Agent (Health monitor)

2. **Full Obsidian Integration**:
   - Complete vault structure with organized folders
   - Rich Dashboard with Dataview queries for real-time monitoring
   - Company Handbook with Obsidian formatting and features
   - Templates for common tasks and processes
   - Proper Obsidian configuration with workspace and plugin settings

3. **Advanced Automation**:
   - Gmail monitoring for important emails
   - File system monitoring for dropped files
   - WhatsApp monitoring for urgent messages
   - Task processing according to company rules

4. **Human-in-the-Loop**:
   - Approval workflow for sensitive actions
   - Clear separation between automated and manual tasks

## 📁 Clean Repository Structure

The repository has been cleaned up to contain only essential files:

- **Core Source Files** in `src/` directory
- **Obsidian Vault** in `obsidian_vault/` directory
- **Main Entry Point** `run_ai_employee.py`
- **Configuration** files: `config.json`, `mcp.json`
- **Environment Variables** in `.env.example`
- **Documentation** in `README.md`
- **Requirements** in `requirements.txt`

## 🗝️ Environment Variables

Create a `.env` file based on `.env.example` to configure API keys and sensitive information:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual API keys and configuration
```

Required environment variables include:
- Gmail API credentials
- WhatsApp session path
- Claude API key (if using Claude directly)
- MCP server configurations
- Security thresholds

## 📁 Enhanced Obsidian Vault Structure

```
obsidian_vault/
├── Inbox/                 # Incoming items to process
├── Needs_Action/          # Items requiring processing
├── Plans/                 # Planned actions
├── Pending_Approval/      # Items requiring human approval
├── Approved/              # Approved items
├── Rejected/              # Rejected items
├── Done/                  # Completed tasks
├── Logs/                  # System logs
├── Attachments/           # File attachments
├── Templates/             # Template files
├── Dashboard.md           # Rich Obsidian dashboard with Dataview queries
├── Company_Handbook.md    # Business rules with Obsidian formatting
└── .obsidian/             # Obsidian configuration
    ├── workspace.json     # Custom workspace layout
    ├── app.json           # App settings
    ├── graph.json         # Graph view settings
    ├── templates.json     # Template settings
    ├── dataview.json      # Dataview plugin configuration
    └── plugins/           # Plugin configurations
        └── obsidian-tasks-plugin/
            └── data.json  # Tasks plugin settings
```

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   npm install # for email MCP server
   ```

2. **Setup**:
   ```bash
   # Install Playwright browsers
   playwright install chromium
   ```

3. **Run the System**:
   ```bash
   # Option 1: Direct Python execution
   python run_ai_employee.py --mode bronze --vault-path obsidian_vault

   # Option 2: Using the startup script (Windows)
   start_ai_employee.bat

   # Option 3: Using the startup script (Unix/Linux/Mac)
   chmod +x start_ai_employee.sh
   ./start_ai_employee.sh
   ```

4. **Open in Obsidian**:
   - Open the `obsidian_vault` folder in Obsidian
   - Recommended plugins: Tasks, Dataview, Templater
   - Monitor system status in `Dashboard.md`

## ⚙️ Configuration

The system can be configured via the `config.json` file. Key configuration options include:

- Check intervals for different watchers
- Security thresholds for approval requirements
- MCP server settings
- Logging levels
- Obsidian integration settings

## 📊 Rich Obsidian Dashboard

Monitor system status in `obsidian_vault/Dashboard.md`, which features:

- Real-time statistics with Dataview queries
- Recent activities tracking
- Pending approvals list
- Quick navigation links
- System health monitoring
- Daily metrics and statistics

## 🛡️ Security Features

- Human approval required for sensitive actions
- Financial transaction limits
- Communication rules enforcement
- Audit logging
- Secure task processing

## 🧠 Comprehensive Company Handbook

The `obsidian_vault/Company_Handbook.md` file contains business rules with Obsidian features:

- Email processing rules
- Financial action requirements
- Communication guidelines
- Approval requirements
- Default actions
- Rich formatting with callouts and lists

## 📝 Obsidian Templates

The system includes templates for common tasks:
- `Task_Template.md` - Standard task template
- `Approval_Request_Template.md` - Approval request template
- `Daily_Note_Template.md` - Daily note template

## 🔄 Continuous Operation

The system runs continuously with:
- Automatic restart of failed processes
- Real-time monitoring
- Self-healing capabilities
- Persistent task processing
- Seamless Obsidian integration

## 🎯 Bronze Tier Completion Criteria Met

✅ Basic architecture implemented with all 5 core agent types
✅ **FULL Obsidian vault integration** with proper folder structure
✅ Gmail watcher for monitoring important emails
✅ File system watcher for dropped files
✅ Task processing according to company handbook rules
✅ Human-in-the-loop approval workflow
✅ **Rich Obsidian dashboard** with Dataview queries for monitoring system status
✅ Basic MCP server for email operations
✅ Watchdog for process monitoring
✅ Continuous operation capability
✅ **Obsidian-specific features**: Callouts, links, queries, templates, and rich formatting

## 🚀 Next Steps

With the bronze tier complete, you can now:
1. Begin testing with real data in the Obsidian vault
2. Install recommended Obsidian plugins (Tasks, Dataview, Templater)
3. Add additional watcher agents (calendar, social media, etc.)
4. Expand the company handbook with more business rules
5. Implement advanced features for silver/gold tiers
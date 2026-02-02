#!/usr/bin/env python3
"""
Main entry point for the Personal AI Employee system.
This script starts all the necessary components for the bronze tier implementation.
"""
import os
import sys
import time
import threading
from pathlib import Path
import argparse

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    # dotenv is optional, so if it's not installed, just continue
    pass

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def create_vault_structure():
    """Create the necessary vault directory structure"""
    vault_path = Path("obsidian_vault")  # Updated to use obsidian vault
    directories = [
        "Inbox",
        "Needs_Action",
        "Plans",
        "Pending_Approval",
        "Approved",
        "Rejected",
        "Done",
        "Logs",
        "Attachments",
        "Templates"
    ]

    for directory in directories:
        (vault_path / directory).mkdir(parents=True, exist_ok=True)

    print(f"Created Obsidian vault structure in {vault_path}")

def create_company_handbook():
    """Create a basic Company Handbook if it doesn't exist"""
    handbook_path = Path("obsidian_vault") / "Company_Handbook.md"

    if not handbook_path.exists():
        handbook_content = """# 📘 Company Handbook

Welcome to the AI Employee's decision-making guide. This handbook defines the rules and procedures that govern how the AI Employee processes tasks and makes decisions.

## 📨 Rules for Processing Emails

> [!tip] Email Processing
> - **Routine Inquiries**: Automated responses to known contacts
> - **Financial Terms**: Flag emails with "payment", "invoice", "money", "transfer", "wire" for human approval
> - **Promotional**: Archive promotional emails after reading
> - **Urgent**: Forward emails with "urgent", "asap", "immediately" to priority queue

### Email Categories

#### Routine Processing
- Appointment confirmations
- Meeting reminders
- Status updates from known systems
- Newsletter subscriptions

#### Require Review
- Financial terms and amounts
- Requests for sensitive information
- Communications from new contacts
- Contract-related discussions

#### Immediate Attention
- Urgent priority indicators
- Time-sensitive deadlines
- Critical system alerts

## 💰 Rules for Financial Actions

> [!caution] Financial Guidelines
> - **All payments** require human approval
> - **Transactions over $100** need review
> - **Log all financial activities** for audit trail

### Approval Thresholds
- **$0-$25**: Automated processing
- **$26-$100**: Manager approval
- **$101+**: Executive approval

## 💬 Rules for Communication

> [!info] Communication Standards
> - **New Contacts**: Never send emails without approval
> - **Professional Tone**: Maintain professional tone in all communications
> - **AI Disclosure**: Disclose AI involvement when required

### Communication Protocols
- Use template responses when possible
- Personalize when necessary
- Follow up on outstanding requests
- Archive completed conversations

## 📋 Approval Requirements

> [!warning] Mandatory Approvals
> The following actions **always require human approval**:

- [[Payment Requests]]
- [[Emails to New Contacts]]
- [[File Sharing Requests]]
- [[Access Permission Changes]]
- [[Confidential Information Sharing]]

## 🔄 Default Actions

> [!todo] Standard Procedures
> - Schedule meetings when possible
- Answer frequently asked questions
- Process routine administrative tasks
- Archive completed tasks

### Task Prioritization
1. **Critical**: System alerts, security issues
2. **High**: Urgent communications, deadlines
3. **Medium**: Routine tasks, follow-ups
4. **Low**: Administrative tasks, archiving

## 🛡️ Security Protocols

- Encrypt sensitive data
- Use secure communication channels
- Maintain audit logs
- Report security incidents

## 📈 Performance Metrics

- Response time targets
- Accuracy measurements
- User satisfaction
- Error rates

## 🔁 Continuous Improvement

Regular reviews of:
- Decision accuracy
- Process efficiency
- User satisfaction
- System performance

---

*Last updated: `= date(now())`*
*Handbook Version: 1.0*
"""
        handbook_path.write_text(handbook_content)
        print(f"Created Company Handbook at {handbook_path}")

def create_dashboard():
    """Create a basic Dashboard if it doesn't exist"""
    dashboard_path = Path("obsidian_vault") / "Dashboard.md"

    if not dashboard_path.exists():
        dashboard_content = """# 🤖 AI Employee Dashboard

> [!info] System Status
> **Active** | Last Updated: {{date}} | Tasks Processed: {{completed-today}}

## 📊 Daily Summary

- **Completed Tasks**: {{completed-today}}
- **Pending Approvals**: {{pending-approvals}}
- **Active Processes**: {{active-processes}}
- **System Health**: {{system-status}}

## 🔄 Recent Activities

```tasks
not done
path includes Inbox
path includes Needs_Action
```

## ⚠️ Pending Approvals

```tasks
not done
path includes Pending_Approval
```

## 📅 Upcoming Actions

- [ ] Review and approve pending requests
- [ ] Process high-priority emails
- [ ] Check system logs for errors

## 📈 Weekly Overview

| Day | Tasks | Approvals | Errors |
|-----|-------|----------|--------|
| Mon |       |          |        |
| Tue |       |          |        |
| Wed |       |          |        |
| Thu |       |          |        |
| Fri |       |          |        |
| Sat |       |          |        |
| Sun |       |          |        |

## 📁 Quick Links

- [[Inbox]]
- [[Needs_Action]]
- [[Pending_Approval]]
- [[Company_Handbook]]

## 🔍 System Information

- **Last Run**: {{last-run}}
- **Version**: Bronze Tier
- **Agents Active**:
  - [{{gmail-watcher-status}}] Gmail Watcher
  - [{{filesystem-watcher-status}}] File System Watcher
  - [{{whatsapp-watcher-status}}] WhatsApp Watcher
  - [{{orchestrator-status}}] Orchestrator
  - [{{watchdog-status}}] Watchdog

---

*Auto-generated dashboard. Last updated: `= date(now())`*
"""
        dashboard_path.write_text(dashboard_content)
        print(f"Created Dashboard at {dashboard_path}")

def main():
    parser = argparse.ArgumentParser(description='Personal AI Employee System')
    parser.add_argument('--mode', choices=['minimal', 'bronze', 'full'], default='bronze',
                       help='Run mode: minimal (core), bronze (hackathon requirements), full (all features)')
    parser.add_argument('--vault-path', default='obsidian_vault',
                       help='Path to the Obsidian vault')

    args = parser.parse_args()

    print("🚀 Starting Personal AI Employee System...")
    print(f"Mode: {args.mode}")
    print(f"Vault: {args.vault_path}")

    # Create necessary structures
    create_vault_structure()
    create_company_handbook()
    create_dashboard()

    # Import the necessary modules
    try:
        from src.agents.orchestrator import Orchestrator
        from src.agents.gmail_watcher import GmailWatcher
        from src.agents.filesystem_watcher import FileSystemWatcher
        from src.agents.whatsapp_watcher import WhatsAppWatcher
        from src.agents.watchdog import WatchdogAgent
        from src.utils.logger import setup_logger
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("Make sure all required dependencies are installed.")
        return

    # Set up logger
    logger = setup_logger("ai_employee", f"{args.vault_path}/Logs/startup.log")
    logger.info("AI Employee System starting up...")

    print("\n📋 Starting Bronze Tier Implementation...")

    # Initialize orchestrator
    orchestrator = Orchestrator(vault_path=args.vault_path)

    if args.mode in ['bronze', 'full']:
        # Start orchestrator in a separate thread
        orchestrator_thread = threading.Thread(
            target=orchestrator.run,
            daemon=True
        )
        orchestrator_thread.start()
        print("✅ Orchestrator started")

        # Initialize and start watchdog
        watchdog = WatchdogAgent(vault_path=args.vault_path)
        watchdog.start_system_monitoring()

        watchdog_thread = threading.Thread(
            target=watchdog.run,
            daemon=True
        )
        watchdog_thread.start()
        print("✅ Watchdog started")

        # Start Gmail watcher if credentials are available
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials

            # Check if Gmail credentials exist
            creds_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'gmail_credentials.json')
            if Path(creds_path).exists():
                gmail_watcher = GmailWatcher(
                    vault_path=args.vault_path,
                    credentials_path=creds_path
                )

                gmail_thread = threading.Thread(
                    target=gmail_watcher.run,
                    daemon=True
                )
                gmail_thread.start()
                print("✅ Gmail Watcher started")
            else:
                print("⚠️  Gmail Watcher skipped (credentials not found)")
        except ImportError:
            print("⚠️  Gmail Watcher skipped (google-api-python-client not installed)")

    print("\n✨ Bronze Tier Implementation Running!")
    print("\n📊 System Components Active:")
    print("   • Orchestrator: Managing task flow")
    print("   • Watchdog: Monitoring system health")
    print("   • Dashboard: Tracking status in vault/Dashboard.md")
    print("   • Company Handbook: Governing decision-making in vault/Company_Handbook.md")
    print("\n📂 Vault Structure:")
    print("   • Needs_Action: Incoming tasks to process")
    print("   • Pending_Approval: Tasks requiring human approval")
    print("   • Done: Completed tasks")
    print("   • Logs: System logs")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AI Employee System...")
        logger.info("AI Employee System shutdown initiated")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
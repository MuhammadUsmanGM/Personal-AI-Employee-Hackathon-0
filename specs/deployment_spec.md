# Deployment Specifications for Personal AI Employee

## Overview
This document outlines the deployment strategies for the Personal AI Employee system across different tiers, from local development to production cloud deployment with local/cloud coordination.

## Deployment Tiers

### Bronze Tier: Local Development
**Target Environment**: Single local machine
**Components**:
- Claude Code on local machine
- Obsidian vault on local storage
- Python watchers running locally
- MCP servers running locally

**Deployment Requirements**:
- Local development environment setup
- Single-user access
- Basic security measures
- Development-focused configuration

### Silver Tier: Enhanced Local
**Target Environment**: Local machine with enhanced capabilities
**Additional Components**:
- Multiple watcher scripts
- MCP server for external actions
- Scheduling capabilities
- Human-in-the-loop approval workflows

### Gold Tier: Autonomous Local
**Target Environment**: Local machine with full autonomous operation
**Additional Components**:
- Full cross-domain integration
- Accounting system integration (Odoo)
- Social media integration
- Comprehensive audit logging
- Ralph Wiggum persistence loops

### Platinum Tier: Hybrid Cloud/Local
**Target Environment**: Cloud VM + Local coordination
**Additional Components**:
- Cloud VM for 24/7 operation
- Synchronized vault system
- Work-zone specialization
- Direct A2A communication

## Local Deployment (Bronze-Silver-Gold)

### Prerequisites
```bash
# Hardware Requirements
- Minimum: 8GB RAM, 4-core CPU, 20GB free disk space
- Recommended: 16GB RAM, 8-core CPU, SSD storage

# Software Requirements
- Claude Code Pro subscription
- Obsidian v1.10.6+
- Python 3.13+
- Node.js v24+ LTS
- GitHub Desktop
```

### Installation Process
```bash
# 1. Clone the repository
git clone https://github.com/user/ai-employee-vault.git

# 2. Create Obsidian vault
mkdir AI_Employee_Vault
cd AI_Employee_Vault

# 3. Initialize vault structure
mkdir Needs_Action Plans Done Pending_Approval Logs Briefings

# 4. Install dependencies
pip install -r requirements.txt
npm install

# 5. Configure environment
cp .env.example .env
# Edit .env with actual credentials
```

### Configuration Files
**Claude Code MCP Configuration** (`~/.config/claude-code/mcp.json`):
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
    }
  ]
}
```

### Startup Sequence
```bash
# 1. Start MCP servers
npm run start-mcp-servers

# 2. Start watchers
python gmail_watcher.py &
python whatsapp_watcher.py &
python filesystem_watcher.py &

# 3. Start orchestrator
python orchestrator.py

# 4. Optional: Start Claude in Ralph loop
claude /ralph-loop "Monitor /Needs_Action and process tasks"
```

### Process Management
Using PM2 for persistent execution:
```bash
# Install PM2
npm install -g pm2

# Start watchers with PM2
pm2 start gmail_watcher.py --name "gmail-watcher" --interpreter python3
pm2 start whatsapp_watcher.py --name "whatsapp-watcher" --interpreter python3
pm2 start filesystem_watcher.py --name "fs-watcher" --interpreter python3
pm2 start orchestrator.py --name "orchestrator" --interpreter python3

# Save and enable startup script
pm2 save
pm2 startup
```

## Cloud Deployment (Platinum)

### Infrastructure Requirements
- Cloud VM (Oracle/AWS/Azure) with:
  - 8GB+ RAM, 4+ cores
  - SSD storage
  - Reliable network connectivity
  - 24/7 uptime SLA

### Cloud VM Setup
```bash
# 1. Provision VM
# Using Oracle Cloud Free Tier (example)
oci compute instance launch \
  --shape VM.Standard.A1.Flex \
  --assign-public-ip true \
  --subnet-id <subnet-id>

# 2. Install prerequisites
sudo apt update && sudo apt upgrade -y
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs python3.13 python3-pip git

# 3. Install Claude Code
npm install -g @anthropic/claude-code
```

### Vault Synchronization
Using Git for secure synchronization:
```bash
# 1. Set up private Git repository
git init
git remote add origin git@github.com:user/secure-ai-vault.git

# 2. Configure .gitignore for security
echo ".env*" >> .gitignore
echo "*.session" >> .gitignore
echo "credentials.json" >> .gitignore
echo "tokens/" >> .gitignore

# 3. Sync strategy
# Local: Master authority for Dashboard.md, secrets never sync
# Cloud: Writes to /Updates/, local merges to Dashboard.md
```

### Work-Zone Specialization
**Cloud Responsibilities**:
- Email triage and draft replies
- Social post drafts and scheduling (draft-only)
- Initial processing of incoming tasks
- 24/7 monitoring and response

**Local Responsibilities**:
- Human approvals
- WhatsApp session management
- Payment/banking operations
- Final "send/post" actions
- Dashboard maintenance

### Security Architecture
```bash
# Vault sync includes only markdown/state
# Secrets never sync (.env, tokens, sessions, banking creds)
# Cloud never stores or uses sensitive credentials

# Example sync script
#!/bin/bash
# sync-vault.sh
rsync -av --exclude="*.env" --exclude="*.session" --exclude="credentials.json" \
  ./ /backup-vault/ --delete
```

## High Availability Setup

### Load Balancing
```bash
# Using nginx for load balancing (if multiple instances)
upstream ai_employee_backend {
    server localhost:3000;
    server localhost:3001 backup;
}
```

### Health Monitoring
```python
# health_check.py
import requests
import psutil
import os

def check_system_health():
    checks = {
        'cpu_usage': psutil.cpu_percent() < 80,
        'memory_usage': psutil.virtual_memory().percent < 80,
        'disk_usage': psutil.disk_usage('/').percent < 80,
        'mcp_servers': check_mcp_connectivity(),
        'watchers_running': check_processes(['gmail_watcher', 'whatsapp_watcher'])
    }
    return all(checks.values()), checks
```

### Backup and Recovery
```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/$(date +%Y-%m-%d)"
mkdir -p $BACKUP_DIR

# Backup vault (excluding sensitive files)
rsync -av --exclude="*.env" --exclude="*.session" \
  /home/user/AI_Employee_Vault/ $BACKUP_DIR/vault/

# Backup logs
tar -czf $BACKUP_DIR/logs.tar.gz /home/user/AI_Employee_Vault/Logs/

# Backup configurations
cp ~/.config/claude-code/mcp.json $BACKUP_DIR/configs/
```

## Monitoring and Observability

### System Metrics
```bash
# Using Prometheus for metrics collection
# prometheus.yml
scrape_configs:
  - job_name: 'ai_employee'
    static_configs:
      - targets: ['localhost:9090']
```

### Logging Configuration
```json
{
  "version": 1,
  "handlers": {
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "filename": "/var/log/ai_employee/app.log",
      "maxBytes": 10485760,
      "backupCount": 5
    }
  },
  "root": {
    "level": "INFO",
    "handlers": ["file"]
  }
}
```

### Alerting Rules
```yaml
# alert_rules.yml
groups:
  - name: ai_employee_alerts
    rules:
      - alert: HighCPUUsage
        expr: cpu_usage > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
```

## Security Hardening

### Network Security
```bash
# Firewall configuration
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

### Service Security
```bash
# Run services with minimal privileges
# Create dedicated user
useradd -r -s /bin/false ai_employee

# Set appropriate permissions
chown -R ai_employee:ai_employee /opt/ai_employee
chmod -R 750 /opt/ai_employee
```

## Scaling Considerations

### Horizontal Scaling
```bash
# Using Docker Compose for scaling
version: '3.8'
services:
  watcher-gmail:
    image: ai-employee/watcher
    command: python gmail_watcher.py
    environment:
      - WATCHER_TYPE=gmail
  watcher-whatsapp:
    image: ai-employee/watcher
    command: python whatsapp_watcher.py
    environment:
      - WATCHER_TYPE=whatsapp
```

### Vertical Scaling
```bash
# Resource allocation based on load
# Small: 2 vCPU, 4GB RAM - Basic operations
# Medium: 4 vCPU, 8GB RAM - Moderate workload
# Large: 8 vCPU, 16GB RAM - Heavy processing
```

## Rollback Procedures

### Version Management
```bash
# Using Git for version control
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0

# Rollback procedure
git checkout v1.0.0
npm install
sudo systemctl restart ai-employee-services
```

### Configuration Rollback
```bash
# Backup configuration before changes
cp /etc/ai-employee/config.json /etc/ai-employee/config.json.backup

# Rollback command
cp /etc/ai-employee/config.json.backup /etc/ai-employee/config.json
sudo systemctl reload ai-employee-services
```

## Maintenance Procedures

### Regular Maintenance Window
```bash
# Weekly maintenance tasks
# Sunday 2-4 AM UTC
0 2 * * 0 /usr/local/bin/maintenance.sh
```

### Update Process
```bash
# 1. Test updates in staging environment
# 2. Deploy to canary instance
# 3. Monitor for 24 hours
# 4. Roll out to production
# 5. Monitor post-deployment metrics
```

## Disaster Recovery

### Recovery Time Objectives
- RTO (Recovery Time Objective): 4 hours for critical systems
- RPO (Recovery Point Objective): 1 hour data loss acceptable

### Recovery Procedures
```bash
# Emergency recovery script
#!/bin/bash
# 1. Restore from latest backup
# 2. Reconfigure services
# 3. Verify system integrity
# 4. Resume operations
```

## Deployment Automation

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy AI Employee
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to server
      run: |
        scp -r ./* user@server:/opt/ai_employee/
        ssh user@server 'sudo systemctl restart ai-employee-services'
```

### Infrastructure as Code
```hcl
# terraform/main.tf
resource "aws_instance" "ai_employee" {
  ami           = var.ami_id
  instance_type = "t3.medium"

  tags = {
    Name = "AI-Employee-VM"
  }
}
```
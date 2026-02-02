# Silver Tier Quickstart Guide - Personal AI Employee System

## Overview
This guide provides instructions for setting up and running the Silver Tier Personal AI Employee system. The Silver Tier enhances the Bronze Tier with advanced automation, extended integrations, enhanced monitoring, and learning capabilities.

## Prerequisites

### System Requirements
- Python 3.13 or higher
- Node.js v24+ LTS
- At least 4GB RAM (8GB recommended)
- 2GB free disk space
- Internet connection for external integrations
- Docker (optional, for containerized deployment)

### External Dependencies
- Gmail account with API access
- WhatsApp account (for WhatsApp monitoring)
- Obsidian installed (for dashboard interface)
- Claude Code CLI (for reasoning engine)

## Installation

### 1. Clone and Setup Repository
```bash
# Clone the repository (if needed)
git clone [repository-url]
cd [repository-name]

# Or update existing Bronze Tier installation
git pull origin master
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

The updated requirements.txt includes:
- All Bronze Tier dependencies
- FastAPI for web API
- SQLAlchemy for data management
- Additional analytics libraries

### 3. Install JavaScript Dependencies
```bash
cd src/mcp-servers/email-mcp-server
npm install
cd ../../..
```

### 4. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your specific configuration:
- API keys for external services
- Database connection strings
- OAuth credentials
- Notification settings

## Configuration

### 1. Update Configuration File
The Silver Tier extends the existing `config.json` with additional settings:

```json
{
  "vault_path": "obsidian_vault",
  "check_interval": {
    "gmail": 120,
    "whatsapp": 30,
    "filesystem": 10,
    "calendar": 300,
    "orchestrator": 60
  },
  "silver_tier_features": {
    "enable_analytics": true,
    "enable_learning": true,
    "enable_advanced_monitoring": true,
    "enable_predictive_features": true
  },
  "api": {
    "host": "localhost",
    "port": 8000,
    "workers": 4
  },
  "database": {
    "url": "sqlite:///silver_tier.db",
    "pool_size": 20,
    "pool_overflow": 10
  },
  "integrations": {
    "calendar_enabled": true,
    "crm_enabled": false,
    "project_management_enabled": false
  }
}
```

### 2. Initialize Database (if using)
```bash
python -c "from src.services.database import init_db; init_db()"
```

## Running the System

### 1. Start the AI Employee System
```bash
# For development
python run_ai_employee.py --mode silver --vault-path obsidian_vault

# For production (with enhanced features)
python run_ai_employee.py --mode silver --vault-path obsidian_vault --enable-analytics --enable-learning
```

### 2. Start the Web API (optional but recommended)
```bash
cd src/api
uvicorn main:app --host localhost --port 8000 --reload
```

### 3. Open in Obsidian
- Open the `obsidian_vault` folder in Obsidian
- Install recommended plugins: Tasks, Dataview, Templater
- Monitor system status in `Dashboard.md`

## Silver Tier Features

### 1. Enhanced Dashboard
The Silver Tier provides an enhanced dashboard with:
- Real-time analytics and metrics
- Predictive task analysis
- User preference learning indicators
- Advanced monitoring panels

### 2. Extended Integrations
- **Calendar Integration**: Monitor and schedule appointments
- **CRM Integration**: Track customer interactions (setup required)
- **Project Management**: Sync with tools like Asana, Trello (setup required)

### 3. Learning Capabilities
- The system learns from your approval patterns
- Adapts to your communication style
- Improves task classification over time

### 4. Advanced Monitoring
- Real-time system health monitoring
- Performance analytics
- Error tracking and resolution
- Usage statistics

## API Endpoints (New in Silver Tier)

### Dashboard API
- `GET /api/dashboard/status` - Current system status
- `GET /api/dashboard/analytics` - Performance analytics
- `GET /api/dashboard/tasks` - Task overview

### Task Management API
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Approval Workflow API
- `GET /api/approvals/pending` - Pending approval requests
- `POST /api/approvals/{id}/approve` - Approve request
- `POST /api/approvals/{id}/reject` - Reject request

## Environment Variables Reference

Key environment variables for Silver Tier:

```bash
# Database Configuration
DATABASE_URL=sqlite:///silver_tier.db

# API Configuration
API_HOST=localhost
API_PORT=8000

# Analytics Configuration
ENABLE_ANALYTICS=true
ANALYTICS_RETENTION_DAYS=90

# Learning Configuration
ENABLE_LEARNING=true
LEARNING_MODEL_VERSION=v1

# Integration Configuration
CALENDAR_INTEGRATION_ENABLED=true
CRM_INTEGRATION_ENABLED=false
PROJECT_MANAGEMENT_ENABLED=false

# Notification Configuration
NOTIFICATION_EMAIL=user@example.com
NOTIFICATION_METHODS=email,slack
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure database file permissions are correct
   - Verify database URL in configuration

2. **API Not Starting**
   - Check if port 8000 is available
   - Verify FastAPI dependencies are installed

3. **Learning Features Not Working**
   - Ensure learning is enabled in config
   - Check that interaction logs are being created

### Checking System Status
```bash
# Check if all services are running
python -c "from src.services.health_check import check_health; print(check_health())"

# View recent logs
tail -f obsidian_vault/Logs/latest.log
```

## Migration from Bronze Tier

The Silver Tier maintains full backward compatibility with Bronze Tier:
- Existing vault structure is preserved
- All Bronze Tier functionality remains
- Configuration files are extended, not replaced
- Data migration is handled automatically

## Next Steps

1. **Configure Integrations**: Set up calendar and other integrations
2. **Train Learning Models**: Allow system to learn from your preferences
3. **Monitor Analytics**: Review the enhanced dashboard metrics
4. **Provide Feedback**: Rate system decisions to improve learning
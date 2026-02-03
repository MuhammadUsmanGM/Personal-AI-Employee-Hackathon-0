# Quickstart Guide: Platinum Tier - Personal AI Employee System

**Date**: 2026-02-03 | **Tier**: Platinum | **Prerequisites**: Gold Tier system installed

## Overview

This quickstart guide provides instructions for setting up and running the Platinum Tier of the Personal AI Employee system, which adds global scale operations, advanced AI orchestration, quantum-safe security, predictive enterprise intelligence, autonomous business operations, blockchain integration, IoT & edge computing, and AR/VR interfaces.

## Prerequisites

- Python 3.13+ installed
- Node.js v24+ LTS installed
- Claude Code CLI installed
- PostgreSQL server (for enterprise analytics)
- Git version control
- Access to quantum-safe cryptography libraries
- Blockchain integration tools
- IoT device management libraries
- AR/VR SDKs and engines
- Completed Gold Tier installation

## Installation Steps

### 1. Clone and Setup Repository

```bash
git clone <repository-url>
cd <repository-directory>

# Install Python dependencies including Platinum Tier additions
pip install quantum-cryptography blockchain-sdk iot-manager ar-vr-sdk fastapi sqlalchemy pydantic transformers torch pandas numpy psycopg2-binary scikit-learn openai sentence-transformers opencv-python pillow librosa faiss-cpu joblib scipy

# Install Node.js dependencies
cd mcp-servers/email-mcp-server
npm install
```

### 2. Configure Environment Variables

Create or update `.env` file with Platinum Tier configurations:

```env
# Base configurations from Gold Tier
PYTHONPATH=./src
VAULT_PATH=./vault
HANDBOOK_PATH=./handbook.md

# Platinum Tier Global Configuration
GLOBAL_REGION=us-east-1
GLOBAL_SCALE_ENABLED=true
MULTI_REGION_SUPPORT=true

# Quantum-Safe Security Configuration
QUANTUM_ENCRYPTION_ENABLED=true
QUANTUM_KEY_ROTATION_INTERVAL=24  # hours
QUANTUM_SECURE_COMMUNICATION=true

# Blockchain Integration Configuration
BLOCKCHAIN_NETWORK=ethereum
BLOCKCHAIN_RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
SMART_CONTRACT_ADDRESS=0x...

# IoT Device Management Configuration
IOT_DEVICE_MANAGER_ENABLED=true
IOT_DEVICE_API_KEY=your_iot_api_key
IOT_DEVICE_CONNECTION_TIMEOUT=30

# AR/VR Interface Configuration
ARVR_INTERFACE_ENABLED=true
ARVR_RENDERING_ENGINE=unity
ARVR_SUPPORTED_PLATFORMS=windows,macos,android

# Global Scaling Configuration
GLOBAL_LOAD_BALANCER=http://global-lb.example.com
REGIONAL_ENDPOINTS=["http://us-east.example.com", "http://eu-west.example.com"]
AUTO_SCALING_ENABLED=true

# PostgreSQL for Enterprise Analytics
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=enterprise_analytics
POSTGRES_USER=analytics_user
POSTGRES_PASSWORD=secure_password

# Advanced AI Configuration
USE_QUANTUM_AI=true
QUANTUM_PROCESSOR_PROVIDER=qiskit
FEDERATED_LEARNING_ENABLED=true
```

### 3. Initialize Database Schema

Run database migrations to create Platinum Tier tables:

```bash
python -m src.utils.database_setup --create-platinum-tables
```

This will create the following Platinum Tier tables:
- `global_operations` - For managing global-scale operations
- `quantum_secure_transactions` - For quantum-safe transactions
- `blockchain_events` - For blockchain event tracking
- `iot_devices` - For IoT device management
- `ar_vr_interfaces` - For AR/VR interface configurations
- `federated_learning_models` - For federated learning model management
- `quantum_computations` - For quantum computation tracking

### 4. Start the Services

#### Start the Main Application Server:

```bash
cd <repository-root>
python -m src.api.main
```

#### Start the MCP Server:

```bash
cd mcp-servers/email-mcp-server
node index.js
```

#### Start the Background Processors:

```bash
# Start the orchestrator
python -m src.agents.orchestrator

# Start the quantum-safe security monitor
python -m src.claude_skills.ai_employee_skills.quantum_security

# Start the IoT device watcher
python -m src.agents.iot_watcher

# Start the blockchain event watcher
python -m src.agents.blockchain_watcher
```

### 5. Configure Obsidian Vault

Add the following to your Obsidian vault to enable Platinum Tier features:

1. Create a new note called `Platinum_Tier_Configuration.md`
2. Add configuration snippets for:
   - Global operations management
   - Quantum-safe security policies
   - Blockchain integration settings
   - IoT device management rules
   - AR/VR interface configurations

Example configuration snippet:

```markdown
## Platinum Tier Configuration

### Global Operations
- Global Operation Categories: [[Strategic Planning]], [[Risk Assessment]], [[Compliance Monitoring]]
- Global Priority Scoring Algorithm: Weighted combination of urgency, impact, and resources required
- Multi-region task distribution enabled

### Quantum Security
- Quantum Key Rotation Schedule: Every 24 hours
- Quantum-safe Encryption Algorithm: Lattice-based cryptography
- Quantum Random Number Generator: Enabled

### Blockchain Integration
- Network: Ethereum Mainnet
- Smart Contract Address: 0x...
- Transaction Verification: Triple-check with multiple nodes
- Audit Trail Recording: Enabled

### IoT Device Management
- Approved Device Types: sensors, actuators, gateways
- Security Level: Quantum-secure
- Data Retention Policy: 7 years for compliance
```

## Running the Platinum Tier System

### Starting the Complete System

Use the following command to start all Platinum Tier components:

```bash
# From repository root
bash scripts/start_platinum_tier.sh
```

Or manually start each component:

```bash
# Terminal 1: Main API server
python -m src.api.main

# Terminal 2: Orchestrator with global capabilities
python -m src.agents.orchestrator --global-mode

# Terminal 3: Quantum security monitor
python -m src.claude_skills.ai_employee_skills.quantum_security

# Terminal 4: IoT device management
python -m src.agents.iot_watcher

# Terminal 5: Blockchain event processing
python -m src.agents.blockchain_watcher

# Terminal 6: AR/VR interface service
python -m src.services.ar_vr_service
```

### Testing Platinum Tier Features

1. **Global Operations**: Submit a task with global scope using the API
   ```bash
   curl -X POST http://localhost:8000/api/global/operations \
     -H "Content-Type: application/json" \
     -d '{"operation_name": "Global Market Analysis", "regions_affected": ["US", "EU", "APAC"], "priority": "high"}'
   ```

2. **Quantum-Safe Transactions**: Test quantum-encrypted communication
   ```bash
   curl -X POST http://localhost:8000/api/quantum/encrypt \
     -H "Content-Type: application/json" \
     -d '{"data": "sensitive information", "security_level": "quantum_safe"}'
   ```

3. **Blockchain Integration**: Verify blockchain transaction processing
   ```bash
   curl -X GET http://localhost:8000/api/blockchain/events
   ```

4. **IoT Device Management**: Register and manage IoT devices
   ```bash
   curl -X POST http://localhost:8000/api/iot/devices/register \
     -H "Content-Type: application/json" \
     -d '{"device_name": "Temperature Sensor 001", "device_type": "sensor", "location_coordinates": {"lat": 40.7128, "lng": -74.0060}}'
   ```

5. **AR/VR Interfaces**: Access AR/VR visualization features
   ```bash
   curl -X GET http://localhost:8000/api/arvr/interfaces
   ```

## Troubleshooting

### Common Issues

1. **Quantum Libraries Not Found**
   - Ensure quantum-safe cryptography libraries are properly installed
   - Check that your Python environment supports the required quantum libraries

2. **Blockchain Connection Failures**
   - Verify blockchain RPC URL and credentials
   - Check network connectivity to blockchain nodes

3. **IoT Device Connection Issues**
   - Confirm IoT device API keys are valid
   - Check network connectivity to IoT device management platform

4. **Global Scaling Performance**
   - Monitor resource usage across regions
   - Adjust auto-scaling configuration as needed

### Platinum Tier Specific Logs

Check these log files for Platinum Tier operations:
- `logs/global_operations.log` - Global operation logs
- `logs/quantum_security.log` - Quantum security logs
- `logs/blockchain_events.log` - Blockchain event logs
- `logs/iot_devices.log` - IoT device management logs
- `logs/ar_vr_interfaces.log` - AR/VR interface logs

## Next Steps

1. Configure your specific business rules in the Obsidian vault
2. Set up global region configurations for your specific use cases
3. Customize quantum security policies based on your compliance requirements
4. Connect IoT devices to the system
5. Set up blockchain wallet and smart contracts
6. Configure AR/VR interfaces for your team's needs
7. Begin migrating from Gold Tier to Platinum Tier functionality

## Support

For support with the Platinum Tier system, please refer to:
- `docs/platinum_tier_guide.md` - Comprehensive Platinum Tier documentation
- `docs/troubleshooting.md` - Troubleshooting guide
- `community/support_channels.md` - Community support options
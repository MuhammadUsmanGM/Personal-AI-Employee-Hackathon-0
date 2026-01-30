# Claude Code Integration Specifications

## Overview
Claude Code serves as the central reasoning engine for the Personal AI Employee, processing inputs from the Obsidian vault, making decisions based on company handbook rules, generating plans, and coordinating with MCP servers for external actions.

## Claude Code Configuration

### Required Setup
- Claude Code Pro subscription or Claude Code Router with free Gemini API
- Local file system access to Obsidian vault
- MCP server connectivity
- Appropriate model selection (claude-4-5-opus recommended)

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

## File System Integration

### Vault Access Permissions
Claude Code requires access to:
- Entire Obsidian vault directory
- /Needs_Action/ folder for incoming tasks
- /Plans/ folder for generated action plans
- /Done/ folder for completed tasks
- /Pending_Approval/ folder for human-in-the-loop approvals
- /Logs/ folder for audit logging
- Dashboard.md for status updates
- Company_Handbook.md for rules and policies
- Business_Goals.md for strategic objectives

### File Processing Patterns
- Monitor /Needs_Action/ for new tasks
- Read Company_Handbook.md for operational rules
- Update Dashboard.md with current status
- Create Plan.md files in /Plans/ directory
- Move processed files to appropriate folders

## Reasoning and Decision Making

### Input Processing
1. **Detection**: Claude identifies new files in /Needs_Action/
2. **Analysis**: Reads file content and extracts relevant information
3. **Context**: Retrieves related information from vault
4. **Decision**: Applies rules from Company_Handbook.md
5. **Planning**: Generates action plan with specific steps

### Rule Application
- Follow guidelines in Company_Handbook.md
- Apply business logic from Business_Goals.md
- Respect permission boundaries defined in security policies
- Implement human-in-the-loop requirements

### Plan Generation
- Create structured Plan.md files with:
  - Clear objectives
  - Step-by-step action items
  - Success criteria
  - Approval requirements
  - Status tracking

## MCP Server Interaction

### Action Orchestration
- Determine appropriate MCP server for each action
- Prepare action parameters according to server specifications
- Execute actions via MCP protocol
- Handle responses and errors appropriately

### Safety Protocols
- Validate all actions before execution
- Implement approval workflows for sensitive operations
- Maintain audit logs for all actions
- Handle failures gracefully

## Ralph Wiggum Persistence Pattern

### Loop Mechanism
```
1. Claude receives initial task
2. Processes task and attempts to exit
3. Stop hook intercepts exit attempt
4. Checks if task completion criteria met
5. If not complete, returns Claude to task
6. Repeats until completion or max iterations
```

### Configuration Options
```
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

### Completion Strategies
- **Promise-based**: Claude outputs `<promise>TASK_COMPLETE</promise>`
- **File movement**: Stop hook detects when task file moves to /Done
- **Status update**: Claude updates status in tracking file

## Human-in-the-Loop Integration

### Approval Workflow
1. Claude identifies action requiring approval
2. Creates approval file in /Pending_Approval/
3. Waits for human intervention
4. Proceeds when file moved to /Approved/
5. Halts when file moved to /Rejected/

### Notification System
- Create clear approval request files
- Include all necessary context
- Specify approval deadline
- Provide rejection alternatives

## Error Handling and Recovery

### Internal Errors
- Handle malformed input files
- Recover from MCP server failures
- Manage API rate limits
- Process invalid configurations

### External Errors
- Handle network connectivity issues
- Manage third-party API failures
- Process authentication errors
- Respond to service unavailability

## Performance Optimization

### Processing Efficiency
- Batch process multiple tasks when possible
- Cache frequently accessed information
- Optimize file system operations
- Minimize redundant API calls

### Resource Management
- Monitor memory usage during extended operations
- Implement proper cleanup procedures
- Manage concurrent operations appropriately
- Optimize model usage for cost-effectiveness

## Security Implementation

### Access Control
- Validate file access permissions
- Implement safe file operation protocols
- Protect against path traversal attacks
- Enforce vault boundary restrictions

### Credential Handling
- Never store credentials in vault
- Use MCP server credential management
- Implement secure parameter passing
- Validate all external connections

## Monitoring and Logging

### Activity Tracking
- Log all Claude Code interactions
- Track MCP server calls and responses
- Monitor processing times and efficiency
- Record decision-making patterns

### Audit Trail
- Maintain chronological record of all actions
- Include human approval decisions
- Track error occurrences and resolutions
- Document system state changes

## Development and Testing

### Development Mode
- Implement DRY_RUN flag to prevent actual actions
- Use test/sandbox accounts for external services
- Enable detailed logging for debugging
- Support incremental testing of components

### Quality Assurance
- Validate output file formats
- Test error recovery procedures
- Verify security constraint enforcement
- Confirm human-in-the-loop workflows

## Integration Points

### With Watchers
- Process files created by watcher scripts
- Update status based on watcher inputs
- Coordinate with watcher health monitoring

### With Obsidian
- Maintain consistent markdown formatting
- Update dashboard in real-time
- Synchronize with vault structure

### With MCP Servers
- Execute actions according to server specifications
- Handle server-specific error conditions
- Maintain connection health monitoring

## Configuration Management

### Environment Variables
- DRY_RUN: Enable/disable actual action execution
- VAULT_PATH: Path to Obsidian vault
- LOG_LEVEL: Logging verbosity level
- MAX_ITERATIONS: Maximum Ralph loop iterations

### Runtime Parameters
- Model selection and configuration
- File processing limits
- Timeout values for external operations
- Retry logic parameters

## Compliance and Governance

### Ethical Guidelines
- Follow established ethical AI principles
- Maintain transparency in AI-assisted communications
- Respect privacy and data protection requirements
- Implement accountability measures

### Regulatory Compliance
- Adhere to applicable data protection laws
- Implement appropriate security measures
- Maintain audit requirements
- Support compliance reporting
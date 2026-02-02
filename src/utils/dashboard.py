import json
from datetime import datetime
from pathlib import Path

def update_dashboard(vault_path, summary_data):
    """
    Update the Dashboard.md file with current status information
    """
    dashboard_path = Path(vault_path) / "Dashboard.md"

    # Create dashboard content
    dashboard_content = f"""# AI Employee Dashboard
Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Today's Summary
- Completed Tasks: {summary_data.get('completed_today', 0)}
- Pending Approvals: {summary_data.get('pending_approvals', 0)}
- System Status: {summary_data.get('system_status', 'active')}
- Errors: {len(summary_data.get('errors', []))}

## Recent Activities
"""

    for activity in summary_data.get('recent_activities', []):
        dashboard_content += f"- {activity}\n"

    if summary_data.get('errors'):
        dashboard_content += "\n## Errors\n"
        for error in summary_data.get('errors', []):
            dashboard_content += f"- {error}\n"

    dashboard_content += f"\nLast Update: {datetime.now().isoformat()}"

    # Write to dashboard file
    dashboard_path.write_text(dashboard_content)
    return dashboard_path

def get_dashboard_summary(vault_path):
    """
    Get current dashboard summary data
    """
    # Count files in various directories
    vault = Path(vault_path)

    needs_action_count = len(list((vault / "Needs_Action").glob("*.md")))
    pending_approval_count = len(list((vault / "Pending_Approval").glob("*.md")))
    completed_today_count = len(list((vault / "Done").glob("*.md")))

    return {
        "completed_today": completed_today_count,
        "pending_approvals": pending_approval_count,
        "needs_action": needs_action_count,
        "system_status": "active",
        "recent_activities": [],
        "errors": []
    }
from pathlib import Path
import time
from datetime import datetime
import sys

# Add the project root to the Python path so imports work correctly
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.vault import VaultEntry, create_vault_entry, move_file_to_folder, get_pending_tasks
from src.utils.handbook_parser import HandbookParser
from src.utils.dashboard import update_dashboard, get_dashboard_summary
from src.utils.logger import log_activity

class TaskProcessor:
    """
    Main processor that reads files from /Inbox/ and processes them according to Company_Handbook rules
    """
    def __init__(self, vault_path="vault", handbook_path=None):
        self.vault_path = Path(vault_path)
        self.handbook_parser = HandbookParser(handbook_path or self.vault_path / "Company_Handbook.md")
        self.inbox_path = self.vault_path / "Inbox"
        self.needs_action_path = self.vault_path / "Needs_Action"
        self.pending_approval_path = self.vault_path / "Pending_Approval"
        self.done_path = self.vault_path / "Done"
        self.plans_path = self.vault_path / "Plans"

    def process_pending_tasks(self):
        """
        Process all pending tasks in the Needs_Action folder
        """
        pending_tasks = get_pending_tasks(self.vault_path)
        processed_count = 0

        for task in pending_tasks:
            try:
                self.process_single_task(task)
                processed_count += 1
            except Exception as e:
                log_activity("ERROR", f"Failed to process task {task.filename}: {str(e)}", self.vault_path)
                # Update task status to error
                task.update_status("error")

        # Update dashboard after processing
        self.update_dashboard()

        return processed_count

    def process_single_task(self, task):
        """
        Process a single task according to company handbook rules
        """
        log_activity("PROCESS", f"Processing task: {task.filename}", self.vault_path)

        # Determine if task needs approval
        needs_approval, reason = self.handbook_parser.should_flag_for_approval(
            task.content, task.type
        )

        if needs_approval:
            # Move to Pending Approval
            self.create_approval_request(task, reason)
            task.update_status("pending_approval")
            move_file_to_folder(
                Path(task.filepath),
                "Pending_Approval",
                self.vault_path
            )
            log_activity("APPROVAL", f"Task {task.filename} requires approval: {reason}", self.vault_path)
        else:
            # Process automatically
            self.execute_automated_task(task)
            task.update_status("completed")
            move_file_to_folder(
                Path(task.filepath),
                "Done",
                self.vault_path
            )
            log_activity("COMPLETED", f"Automatically processed task: {task.filename}", self.vault_path)

    def create_approval_request(self, task, reason):
        """
        Create an approval request for sensitive actions
        """
        approval_content = f"""---
type: approval_request
action: process_task
related_task: {task.filename}
reason: {reason}
created: {datetime.now().isoformat()}
status: pending
---

## Approval Request for Task: {task.filename}

### Original Task Content
{task.content[:500]}...

### Reason for Approval
{reason}

## Action Details
- Task Type: {task.type}
- Priority: {task.frontmatter.get('priority', 'medium')}
- Created: {task.frontmatter.get('created', 'unknown')}

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
"""

        # Create approval request file
        approval_filename = f"APPROVAL_{task.filename.replace('.md', '.md')}"
        create_vault_entry(
            self.vault_path,
            "Pending_Approval",
            approval_filename,
            approval_content,
            entry_type="approval_request",
            priority=task.frontmatter.get('priority', 'medium')
        )

    def execute_automated_task(self, task):
        """
        Execute an automated task (placeholder for actual execution logic)
        """
        # This is where we would implement the actual task execution
        # For now, we just log that it was processed
        log_activity("AUTOMATED", f"Executed automated task: {task.filename}", self.vault_path)

    def process_approval_requests(self):
        """
        Process approval requests that have been moved to Approved/Rejected folders
        """
        approved_path = self.vault_path / "Approved"
        rejected_path = self.vault_path / "Rejected"

        # Process approved requests
        for approved_file in approved_path.glob("*.md"):
            self.handle_approved_request(approved_file)

        # Process rejected requests
        for rejected_file in rejected_path.glob("*.md"):
            self.handle_rejected_request(rejected_file)

    def handle_approved_request(self, approved_file):
        """
        Handle an approved request
        """
        log_activity("APPROVED", f"Handling approved request: {approved_file.name}", self.vault_path)

        # Move the original task back to needs action for execution
        # Extract original task name from approval request
        content = approved_file.read_text()

        # Find the related task in the original content
        import re
        match = re.search(r'related_task: (.+)', content)
        if match:
            original_task_name = match.group(1).strip()
            original_task_path = self.vault_path / "Pending_Approval" / original_task_name

            if original_task_path.exists():
                # Move the original task to needs action for processing
                move_file_to_folder(
                    original_task_path,
                    "Needs_Action",
                    self.vault_path
                )

        # Move approval file to done
        move_file_to_folder(
            approved_file,
            "Done",
            self.vault_path
        )

    def handle_rejected_request(self, rejected_file):
        """
        Handle a rejected request
        """
        log_activity("REJECTED", f"Handling rejected request: {rejected_file.name}", self.vault_path)

        # Move approval file to done
        move_file_to_folder(
            rejected_file,
            "Done",
            self.vault_path
        )

    def update_dashboard(self):
        """
        Update the dashboard with current status
        """
        summary_data = get_dashboard_summary(self.vault_path)
        summary_data['recent_activities'] = [
            f"Processed {len(get_pending_tasks(self.vault_path))} pending tasks",
            f"Updated at {datetime.now().strftime('%H:%M:%S')}"
        ]
        update_dashboard(self.vault_path, summary_data)

    def run_continuous_processing(self, interval=300):  # Default to 5 minutes
        """
        Run continuous processing loop
        """
        log_activity("SYSTEM", "Starting continuous processing loop", self.vault_path)

        while True:
            try:
                # Process pending tasks
                processed_count = self.process_pending_tasks()

                # Process approval requests
                self.process_approval_requests()

                # Update dashboard
                self.update_dashboard()

                log_activity("SYSTEM", f"Completed processing cycle, processed {processed_count} tasks", self.vault_path)

                time.sleep(interval)
            except Exception as e:
                log_activity("ERROR", f"Error in processing loop: {str(e)}", self.vault_path)
                time.sleep(60)  # Wait 1 minute before retrying if there's an error
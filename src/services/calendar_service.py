"""
Calendar Integration Service for Silver Tier Personal AI Employee System
Handles calendar events and appointment scheduling
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid

from .database import IntegrationConnection, Task
from .task_service import TaskService
from ..utils.logger import log_activity


class CalendarProvider(Enum):
    GOOGLE = "google_calendar"
    OUTLOOK = "outlook"
    APPLE = "apple_calendar"
    GENERIC_CALDAV = "caldav"


class CalendarEventStatus(Enum):
    CONFIRMED = "confirmed"
    TENTATIVE = "tentative"
    CANCELLED = "cancelled"


class CalendarEventType(Enum):
    MEETING = "meeting"
    APPOINTMENT = "appointment"
    DEADLINE = "deadline"
    REMINDER = "reminder"
    RECURRING = "recurring"


class CalendarService:
    """
    Service for calendar integration and event management in Silver Tier
    """

    def __init__(self, db_session):
        self.db = db_session
        self.task_service = TaskService(db_session)

    def connect_calendar(self, user_id: str, provider: str, credentials: Dict[str, Any]) -> bool:
        """
        Connect to a calendar service

        Args:
            user_id: User identifier
            provider: Calendar provider (google_calendar, outlook, etc.)
            credentials: Calendar service credentials

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Validate provider
            if provider not in [p.value for p in CalendarProvider]:
                raise ValueError(f"Unsupported calendar provider: {provider}")

            # Check if connection already exists
            existing_connection = self.db.query(IntegrationConnection).filter(
                IntegrationConnection.user_id == user_id,
                IntegrationConnection.service_name == provider
            ).first()

            if existing_connection:
                # Update existing connection
                existing_connection.auth_token = credentials.get('auth_token', existing_connection.auth_token)
                existing_connection.refresh_token = credentials.get('refresh_token', existing_connection.refresh_token)
                existing_connection.connection_status = 'connected'
                existing_connection.updated_at = datetime.utcnow()
            else:
                # Create new connection
                connection = IntegrationConnection(
                    id=str(uuid.uuid4()),
                    service_name=provider,
                    user_id=user_id,
                    connection_status='connected',
                    auth_token=credentials.get('auth_token'),
                    refresh_token=credentials.get('refresh_token'),
                    scopes=credentials.get('scopes', []),
                    last_sync_at=None,
                    sync_frequency_minutes=credentials.get('sync_frequency_minutes', 15),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                self.db.add(connection)

            self.db.commit()

            log_activity("CALENDAR_CONNECTED",
                       f"Calendar {provider} connected for user {user_id}",
                       "obsidian_vault")

            return True
        except Exception as e:
            self.db.rollback()
            log_activity("CALENDAR_CONNECTION_ERROR",
                       f"Error connecting calendar {provider} for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return False

    def disconnect_calendar(self, user_id: str, provider: str) -> bool:
        """
        Disconnect from a calendar service

        Args:
            user_id: User identifier
            provider: Calendar provider to disconnect

        Returns:
            True if disconnection successful, False otherwise
        """
        try:
            connection = self.db.query(IntegrationConnection).filter(
                IntegrationConnection.user_id == user_id,
                IntegrationConnection.service_name == provider
            ).first()

            if not connection:
                return False

            connection.connection_status = 'disconnected'
            connection.updated_at = datetime.utcnow()

            self.db.commit()

            log_activity("CALENDAR_DISCONNECTED",
                       f"Calendar {provider} disconnected for user {user_id}",
                       "obsidian_vault")

            return True
        except Exception as e:
            self.db.rollback()
            log_activity("CALENDAR_DISCONNECTION_ERROR",
                       f"Error disconnecting calendar {provider} for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return False

    def sync_calendar_events(self, user_id: str, provider: str) -> bool:
        """
        Sync calendar events from the connected calendar service

        Args:
            user_id: User identifier
            provider: Calendar provider

        Returns:
            True if sync successful, False otherwise
        """
        try:
            # Check if connection exists and is active
            connection = self.db.query(IntegrationConnection).filter(
                IntegrationConnection.user_id == user_id,
                IntegrationConnection.service_name == provider,
                IntegrationConnection.connection_status == 'connected'
            ).first()

            if not connection:
                log_activity("CALENDAR_SYNC_ERROR",
                           f"No active connection for {provider} and user {user_id}",
                           "obsidian_vault")
                return False

            # In a real implementation, this would call the calendar API
            # For now, we'll simulate getting events
            simulated_events = self._get_simulated_events()

            # Process each event and create tasks if needed
            for event in simulated_events:
                self._process_calendar_event(event, user_id)

            # Update sync timestamp
            connection.last_sync_at = datetime.utcnow()
            self.db.commit()

            log_activity("CALENDAR_SYNCED",
                       f"Synced calendar events for user {user_id} from {provider}",
                       "obsidian_vault")

            return True
        except Exception as e:
            self.db.rollback()
            log_activity("CALENDAR_SYNC_ERROR",
                       f"Error syncing calendar {provider} for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return False

    def _get_simulated_events(self) -> List[Dict[str, Any]]:
        """
        Simulate getting calendar events from API
        In a real implementation, this would call the actual calendar API
        """
        # Simulate calendar events
        now = datetime.utcnow()
        return [
            {
                "id": str(uuid.uuid4()),
                "title": "Team Standup Meeting",
                "description": "Daily team standup to discuss progress and blockers",
                "start_time": now + timedelta(hours=2),
                "end_time": now + timedelta(hours=2, minutes=30),
                "location": "Conference Room A",
                "attendees": ["team@example.com"],
                "status": "confirmed",
                "type": "meeting",
                "organizer": "manager@example.com"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Client Call - Q4 Review",
                "description": "Quarterly review call with key client",
                "start_time": now + timedelta(days=1, hours=10),
                "end_time": now + timedelta(days=1, hours=11),
                "location": "Online",
                "attendees": ["client@example.com", "manager@example.com"],
                "status": "confirmed",
                "type": "meeting",
                "organizer": "scheduler@example.com"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Project Deadline",
                "description": "Final submission deadline for Q4 project",
                "start_time": now + timedelta(days=3),
                "end_time": now + timedelta(days=3),
                "location": "Office",
                "attendees": [],
                "status": "confirmed",
                "type": "deadline",
                "organizer": "project-manager@example.com"
            }
        ]

    def _process_calendar_event(self, event: Dict[str, Any], user_id: str):
        """
        Process a calendar event and create relevant tasks

        Args:
            event: Calendar event data
            user_id: User identifier
        """
        event_type = event.get("type", "meeting").lower()
        start_time = event["start_time"]

        # Determine if we need to create tasks based on event type and time
        time_until_event = start_time - datetime.utcnow()

        # Create preparation tasks for meetings and appointments
        if event_type in ["meeting", "appointment"] and time_until_event.days <= 7:
            # Create preparation task 1 day before
            prep_deadline = start_time - timedelta(days=1)
            if prep_deadline > datetime.utcnow():
                self.task_service.create_task(
                    title=f"Prepare for: {event['title']}",
                    description=f"Prepare materials and agenda for {event['title']}. Event: {event.get('description', 'No description')}",
                    status="pending",
                    priority="high" if time_until_event.days <= 2 else "medium",
                    category="calendar",
                    source="calendar",
                    assigned_to=user_id,
                    due_date=prep_deadline,
                    metadata={
                        "calendar_event_id": event["id"],
                        "event_type": event_type,
                        "event_datetime": start_time.isoformat(),
                        "location": event.get("location", "Not specified"),
                        "attendees": event.get("attendees", [])
                    },
                    estimated_duration=60  # 1 hour to prepare
                )

        # Create reminder tasks
        if time_until_event.days <= 2:
            # Create reminder 1 hour before event
            reminder_time = start_time - timedelta(hours=1)
            if reminder_time > datetime.utcnow():
                self.task_service.create_task(
                    title=f"Reminder: {event['title']}",
                    description=f"Reminder for upcoming event: {event['title']}",
                    status="pending",
                    priority="high",
                    category="calendar",
                    source="calendar",
                    assigned_to=user_id,
                    due_date=reminder_time,
                    metadata={
                        "calendar_event_id": event["id"],
                        "event_type": event_type,
                        "event_datetime": start_time.isoformat(),
                        "action": "reminder"
                    },
                    estimated_duration=5  # 5 minutes to prepare
                )

        # For deadlines, create more aggressive task management
        if event_type == "deadline":
            # Create progress check-ins leading up to deadline
            days_before = min(5, time_until_event.days)  # Max 5 days before
            for i in range(max(1, days_before), 0, -1):
                checkin_time = start_time - timedelta(days=i)
                if checkin_time > datetime.utcnow():
                    self.task_service.create_task(
                        title=f"Progress Check: {event['title']} (Day -{i})",
                        description=f"Check progress on {event['title']} with {i} days remaining",
                        status="pending",
                        priority="medium",
                        category="calendar",
                        source="calendar",
                        assigned_to=user_id,
                        due_date=checkin_time,
                        metadata={
                            "calendar_event_id": event["id"],
                            "event_type": event_type,
                            "event_datetime": start_time.isoformat(),
                            "action": "progress_check"
                        },
                        estimated_duration=15
                    )

    def create_calendar_event(self, user_id: str, event_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a calendar event

        Args:
            user_id: User identifier
            event_data: Event data including title, time, attendees, etc.

        Returns:
            Event ID if created successfully, None otherwise
        """
        try:
            # Validate required fields
            required_fields = ["title", "start_time", "end_time"]
            for field in required_fields:
                if field not in event_data:
                    raise ValueError(f"Missing required field: {field}")

            # Check if user has calendar connected
            connection = self.db.query(IntegrationConnection).filter(
                IntegrationConnection.user_id == user_id,
                IntegrationConnection.connection_status == 'connected'
            ).first()

            if not connection:
                log_activity("EVENT_CREATION_ERROR",
                           f"No calendar connection for user {user_id}",
                           "obsidian_vault")
                return None

            # In a real implementation, this would call the calendar API
            # For simulation, we'll just return a success
            event_id = str(uuid.uuid4())

            # Create a task to confirm the event was scheduled
            self.task_service.create_task(
                title=f"Confirmed: {event_data['title']}",
                description=f"Event '{event_data['title']}' has been scheduled",
                status="completed",
                priority="low",
                category="calendar",
                source="calendar",
                assigned_to=user_id,
                due_date=event_data.get("start_time"),
                metadata={
                    "calendar_event_id": event_id,
                    "event_data": event_data,
                    "action": "confirmation"
                },
                estimated_duration=0
            )

            log_activity("EVENT_CREATED",
                       f"Event '{event_data['title']}' created for user {user_id}",
                       "obsidian_vault")

            return event_id
        except Exception as e:
            log_activity("EVENT_CREATION_ERROR",
                       f"Error creating event for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return None

    def get_upcoming_events(self, user_id: str, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        Get upcoming calendar events for a user

        Args:
            user_id: User identifier
            days_ahead: Number of days to look ahead

        Returns:
            List of upcoming events
        """
        try:
            # In a real implementation, this would query the calendar API
            # For simulation, we'll return some sample events
            now = datetime.utcnow()
            end_date = now + timedelta(days=days_ahead)

            # Simulated events for the user
            simulated_events = [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Team Meeting",
                    "description": "Weekly team sync",
                    "start_time": now + timedelta(days=1, hours=10),
                    "end_time": now + timedelta(days=1, hours=11),
                    "location": "Conference Room B",
                    "attendees": ["team@example.com"],
                    "status": "confirmed",
                    "type": "meeting"
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Client Presentation",
                    "description": "Present Q4 results to client",
                    "start_time": now + timedelta(days=3, hours=14),
                    "end_time": now + timedelta(days=3, hours=15),
                    "location": "Online",
                    "attendees": ["client@example.com"],
                    "status": "confirmed",
                    "type": "meeting"
                }
            ]

            # Filter events within the specified date range
            upcoming_events = []
            for event in simulated_events:
                if now < event["start_time"] <= end_date:
                    upcoming_events.append(event)

            log_activity("UPCOMING_EVENTS_FETCHED",
                       f"Fetched {len(upcoming_events)} upcoming events for user {user_id}",
                       "obsidian_vault")

            return upcoming_events
        except Exception as e:
            log_activity("UPCOMING_EVENTS_ERROR",
                       f"Error fetching upcoming events for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return []

    def get_calendar_connection_status(self, user_id: str, provider: str) -> str:
        """
        Get the connection status for a specific calendar provider

        Args:
            user_id: User identifier
            provider: Calendar provider

        Returns:
            Connection status ('connected', 'disconnected', 'error', 'pending_auth')
        """
        connection = self.db.query(IntegrationConnection).filter(
            IntegrationConnection.user_id == user_id,
            IntegrationConnection.service_name == provider
        ).first()

        if not connection:
            return "disconnected"

        return connection.connection_status

    def schedule_appointment(self, user_id: str, appointment_data: Dict[str, Any]) -> Optional[str]:
        """
        Schedule an appointment based on user availability and preferences

        Args:
            user_id: User identifier
            appointment_data: Appointment details including participant, duration, preferences

        Returns:
            Appointment ID if scheduled successfully, None otherwise
        """
        try:
            # Get user's calendar connections
            connections = self.db.query(IntegrationConnection).filter(
                IntegrationConnection.user_id == user_id,
                IntegrationConnection.connection_status == 'connected'
            ).all()

            if not connections:
                log_activity("APPOINTMENT_SCHEDULING_ERROR",
                           f"No calendar connections for user {user_id}",
                           "obsidian_vault")
                return None

            # In a real implementation, this would:
            # 1. Check user's availability
            # 2. Find suitable time slots
            # 3. Send invitations
            # 4. Confirm the appointment

            # For simulation, we'll schedule a time
            requested_duration = appointment_data.get("duration_minutes", 60)
            requested_participants = appointment_data.get("participants", [])

            # Find a suitable time (simulated)
            suggested_time = datetime.utcnow() + timedelta(days=1, hours=15)  # Tomorrow at 3 PM

            # Create the appointment event
            event_data = {
                "title": appointment_data.get("title", "Scheduled Appointment"),
                "description": appointment_data.get("description", ""),
                "start_time": suggested_time,
                "end_time": suggested_time + timedelta(minutes=requested_duration),
                "attendees": requested_participants,
                "location": appointment_data.get("location", "Online"),
                "status": "confirmed",
                "type": "appointment"
            }

            appointment_id = self.create_calendar_event(user_id, event_data)

            if appointment_id:
                # Create a follow-up task to confirm attendance
                self.task_service.create_task(
                    title=f"Confirm Appointment: {event_data['title']}",
                    description=f"Confirm attendance for scheduled appointment",
                    status="pending",
                    priority="medium",
                    category="calendar",
                    source="calendar",
                    assigned_to=user_id,
                    due_date=suggested_time - timedelta(hours=24),
                    metadata={
                        "calendar_event_id": appointment_id,
                        "appointment_data": appointment_data,
                        "action": "attendance_confirmation"
                    },
                    estimated_duration=5
                )

            log_activity("APPOINTMENT_SCHEDULED",
                       f"Appointment scheduled for user {user_id}",
                       "obsidian_vault")

            return appointment_id
        except Exception as e:
            log_activity("APPOINTMENT_SCHEDULING_ERROR",
                       f"Error scheduling appointment for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return None

    def get_availability(self, user_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Get user's availability between specified dates

        Args:
            user_id: User identifier
            start_date: Start of availability period
            end_date: End of availability period

        Returns:
            List of available time slots
        """
        try:
            # In a real implementation, this would query the calendar API
            # to find free time slots between the dates
            # For simulation, we'll return some available slots

            # Simulated busy times (these would come from actual calendar events)
            busy_slots = [
                {"start": start_date + timedelta(days=1, hours=9), "end": start_date + timedelta(days=1, hours=11)},
                {"start": start_date + timedelta(days=2, hours=14), "end": start_date + timedelta(days=2, hours=16)},
                {"start": start_date + timedelta(days=3, hours=10), "end": start_date + timedelta(days=3, hours=12)},
            ]

            # Calculate available slots
            available_slots = []
            current = start_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Start of business day

            while current.date() <= end_date.date():
                # Define business hours (9 AM to 6 PM)
                day_start = current.replace(hour=9, minute=0)
                day_end = current.replace(hour=18, minute=0)

                # Find available time in this day
                day_available_start = day_start
                for busy in busy_slots:
                    if busy["start"].date() == current.date():
                        # If there's free time before this busy slot
                        if day_available_start < busy["start"]:
                            available_slots.append({
                                "start": day_available_start,
                                "end": busy["start"]
                            })

                        # Update available start time after busy slot
                        day_available_start = busy["end"]

                # Add remaining available time at end of day
                if day_available_start < day_end:
                    available_slots.append({
                        "start": day_available_start,
                        "end": day_end
                    })

                # Move to next day
                current += timedelta(days=1)

            # Filter only future slots
            now = datetime.utcnow()
            future_slots = [slot for slot in available_slots if slot["end"] > now]

            log_activity("AVAILABILITY_FETCHED",
                       f"Fetched availability for user {user_id} ({len(future_slots)} slots)",
                       "obsidian_vault")

            return future_slots
        except Exception as e:
            log_activity("AVAILABILITY_ERROR",
                       f"Error fetching availability for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return []
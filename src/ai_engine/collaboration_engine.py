"""
Human-AI Collaboration Engine for Gold Tier Personal AI Employee System
Implements advanced interaction, communication, and collaboration features
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import asyncio
import re
from enum import Enum

from ..utils.logger import log_activity


class InteractionMode(Enum):
    AUTONOMOUS = "autonomous"
    ASSISTIVE = "assistive"
    COLLABORATIVE = "collaborative"
    SUPERVISED = "supervised"


class CommunicationStyle(Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    DIRECT = "direct"
    POLITE = "polite"
    TECHNICAL = "technical"
    NON_TECHNICAL = "non_technical"


class Emotion(Enum):
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    SATISFIED = "satisfied"


class CollaborationEngine:
    """
    Advanced human-AI collaboration engine for Gold Tier AI capabilities
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # User profiles and preferences
        self.user_profiles = {}
        self.conversation_history = []
        self.emotion_tracking = {}
        self.communication_preferences = {}

        # Collaboration state
        self.current_mode = InteractionMode.ASSISTIVE
        self.active_tasks = []
        self.pending_decisions = []

    def analyze_user_emotion(self, text: str) -> Emotion:
        """
        Analyze the emotional tone of user input

        Args:
            text: User input text

        Returns:
            Detected emotion
        """
        # Simple keyword-based emotion detection
        # In a real system, this would use more sophisticated NLP
        text_lower = text.lower()

        positive_keywords = ['good', 'great', 'excellent', 'thank', 'please', 'appreciate', 'love', 'perfect']
        negative_keywords = ['bad', 'terrible', 'hate', 'annoying', 'frustrated', 'angry', 'worst', 'disappointed']
        confused_keywords = ['confused', 'unclear', 'not sure', 'what do you mean', 'explain', 'how', '?']
        frustrated_keywords = ['why', 'not working', 'broken', 'fix', 'problem', 'issue', 'error']

        positive_score = sum(1 for word in positive_keywords if word in text_lower)
        negative_score = sum(1 for word in negative_keywords if word in text_lower)
        confused_score = sum(1 for word in confused_keywords if word in text_lower)
        frustrated_score = sum(1 for word in frustrated_keywords if word in text_lower)

        # Determine emotion based on scores
        if frustrated_score > 0 or negative_score >= 2:
            return Emotion.FRUSTRATED
        elif confused_score > 0:
            return Emotion.CONFUSED
        elif positive_score >= 2:
            return Emotion.POSITIVE
        elif negative_score > 0:
            return Emotion.NEGATIVE
        else:
            return Emotion.NEUTRAL

    def adapt_communication_style(self, user_id: str, emotion: Emotion) -> CommunicationStyle:
        """
        Adapt communication style based on user emotion and preferences

        Args:
            user_id: ID of the user
            emotion: Current detected emotion

        Returns:
            Recommended communication style
        """
        # Get user preferences
        user_prefs = self.user_profiles.get(user_id, {})
        preferred_style = user_prefs.get('communication_style', CommunicationStyle.FORMAL.value)

        # Adjust style based on emotion
        if emotion == Emotion.FRUSTRATED:
            return CommunicationStyle.DIRECT  # Be direct to resolve quickly
        elif emotion == Emotion.CONFUSED:
            return CommunicationStyle.TECHNICAL  # Be more detailed to clarify
        elif emotion == Emotion.POSITIVE:
            return CommunicationStyle.CASUAL  # Be more relaxed
        elif emotion == Emotion.NEGATIVE:
            return CommunicationStyle.POLITE  # Be extra polite
        else:
            # Use user preference if available
            try:
                return CommunicationStyle(preferred_style)
            except ValueError:
                return CommunicationStyle.FORMAL  # Default

    def generate_response(self, user_input: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        Generate an appropriate response to user input

        Args:
            user_input: User's input text
            user_id: ID of the user

        Returns:
            Response dictionary with text and metadata
        """
        # Analyze emotion
        emotion = self.analyze_user_emotion(user_input)

        # Adapt communication style
        style = self.adapt_communication_style(user_id, emotion)

        # Track emotion for this user
        if user_id not in self.emotion_tracking:
            self.emotion_tracking[user_id] = []
        self.emotion_tracking[user_id].append({
            'emotion': emotion.value,
            'timestamp': datetime.now(),
            'input': user_input
        })

        # Generate response based on style
        response_text = self._compose_response(user_input, style, emotion)

        # Update conversation history
        self.conversation_history.append({
            'user_id': user_id,
            'user_input': user_input,
            'ai_response': response_text,
            'emotion': emotion.value,
            'style': style.value,
            'timestamp': datetime.now()
        })

        response = {
            'response_text': response_text,
            'emotion_detected': emotion.value,
            'communication_style': style.value,
            'confidence': 0.85,  # Default confidence
            'suggested_next_actions': self._suggest_next_actions(user_input, user_id),
            'needs_clarification': self._check_needs_clarification(user_input)
        }

        log_activity("COLLABORATION_RESPONSE", f"Generated response for user {user_id} in {style.value} style", "obsidian_vault")
        return response

    def _compose_response(self, user_input: str, style: CommunicationStyle, emotion: Emotion) -> str:
        """Compose response based on style and emotion"""
        if style == CommunicationStyle.FORMAL:
            if emotion == Emotion.POSITIVE:
                return f"I appreciate your positive feedback regarding '{user_input}'. How may I further assist you today?"
            elif emotion == Emotion.NEGATIVE:
                return f"I acknowledge your concerns about '{user_input}'. I will address this matter with the utmost attention."
            elif emotion == Emotion.FRUSTRATED:
                return f"I understand you may be experiencing frustration. Allow me to provide a direct solution to your query: {user_input}."
            else:
                return f"Thank you for your inquiry: '{user_input}'. I will process this request efficiently."

        elif style == CommunicationStyle.CASUAL:
            if emotion == Emotion.POSITIVE:
                return f"Nice! So you're saying '{user_input}'. Cool, I can definitely help with that!"
            elif emotion == Emotion.NEGATIVE:
                return f"Oh no, that sounds frustrating. Let me see how I can help with '{user_input}'."
            else:
                return f"Got it! So about '{user_input}', I can help you with that."

        elif style == CommunicationStyle.DIRECT:
            return f"Regarding '{user_input}': I will proceed with the following action..."

        elif style == CommunicationStyle.POLITE:
            if emotion == Emotion.FRUSTRATED:
                return f"I sincerely apologize for any inconvenience caused. Regarding '{user_input}', I will resolve this promptly."
            else:
                return f"With respect to '{user_input}', I am happy to assist you in any way possible."

        elif style == CommunicationStyle.TECHNICAL:
            return f"Analyzing input: '{user_input}'. Identified parameters and initiating processing with optimal configuration."

        else:  # NON_TECHNICAL
            return f"So you're asking about '{user_input}'. Let me explain that in simple terms..."

    def _suggest_next_actions(self, user_input: str, user_id: str) -> List[str]:
        """Suggest next actions based on user input"""
        # Analyze the input to suggest relevant actions
        input_lower = user_input.lower()

        suggestions = []

        if any(word in input_lower for word in ['schedule', 'meeting', 'appointment']):
            suggestions.extend([
                "Schedule a meeting",
                "Check calendar availability",
                "Send meeting invitation"
            ])
        elif any(word in input_lower for word in ['email', 'send', 'message']):
            suggestions.extend([
                "Draft email response",
                "Send email to contacts",
                "Check email status"
            ])
        elif any(word in input_lower for word in ['task', 'todo', 'do']):
            suggestions.extend([
                "Create new task",
                "Update existing task",
                "Check task status"
            ])
        elif any(word in input_lower for word in ['report', 'analytics', 'data']):
            suggestions.extend([
                "Generate report",
                "Analyze data",
                "Visualize metrics"
            ])
        elif any(word in input_lower for word in ['approval', 'approve', 'permission']):
            suggestions.extend([
                "Request approval",
                "Check approval status",
                "Escalate for approval"
            ])
        else:
            # General suggestions
            suggestions.extend([
                "Clarify requirements",
                "Provide more details",
                "Check related tasks",
                "Consult documentation"
            ])

        return suggestions[:3]  # Return top 3 suggestions

    def _check_needs_clarification(self, user_input: str) -> bool:
        """Check if user input needs clarification"""
        # Look for ambiguous terms or questions
        ambiguous_patterns = [
            r'it', r'that', r'this', r'these', r'those',  # Vague references
            r'what.*exactly', r'be.*specific', r'clarify',  # Requests for clarification
            r'how.*exactly', r'where.*exactly', r'when.*exactly',  # Specificity requests
            r'more details', r'elaborate', r'explain',  # Explanation requests
            r'unsure', r'not sure', r'unclear',  # Uncertainty indicators
        ]

        input_lower = user_input.lower()
        for pattern in ambiguous_patterns:
            if re.search(pattern, input_lower):
                return True

        # Check if input is very short (might be unclear)
        words = user_input.split()
        if len(words) < 3:
            return True

        return False

    def set_interaction_mode(self, mode: InteractionMode, user_id: str = "default_user"):
        """
        Set the interaction mode for collaboration

        Args:
            mode: Desired interaction mode
            user_id: ID of the user
        """
        self.current_mode = mode

        # Update user profile with preferred mode
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        self.user_profiles[user_id]['interaction_mode'] = mode.value

        log_activity("INTERACTION_MODE_SET", f"Set interaction mode to {mode.value} for user {user_id}", "obsidian_vault")

    def initiate_collaboration(self, task_description: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        Initiate a collaborative task with the user

        Args:
            task_description: Description of the task to collaborate on
            user_id: ID of the user

        Returns:
            Collaboration initiation details
        """
        collaboration_id = f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"

        collaboration = {
            'id': collaboration_id,
            'task_description': task_description,
            'user_id': user_id,
            'started_at': datetime.now(),
            'status': 'initiated',
            'interaction_mode': self.current_mode.value,
            'steps': [],
            'progress': 0.0,
            'estimated_completion': None,
            'required_inputs': self._extract_required_inputs(task_description),
            'suggested_approach': self._suggest_approach(task_description)
        }

        # Add to active collaborations
        self.active_tasks.append(collaboration)

        response = {
            'collaboration_id': collaboration_id,
            'status': 'initiated',
            'message': f"I've understood your task: '{task_description}'. Let's work on this together!",
            'required_inputs': collaboration['required_inputs'],
            'suggested_approach': collaboration['suggested_approach'],
            'next_steps': ['Provide additional details', 'Confirm approach', 'Begin execution']
        }

        log_activity("COLLABORATION_INITIATED", f"Started collaboration on: {task_description[:50]}...", "obsidian_vault")
        return response

    def _extract_required_inputs(self, task_description: str) -> List[str]:
        """Extract required inputs from task description"""
        # Simple keyword extraction for required inputs
        description_lower = task_description.lower()

        required_inputs = []

        if 'email' in description_lower:
            required_inputs.append('Email addresses')
        if 'date' in description_lower or 'time' in description_lower:
            required_inputs.append('Specific date/time')
        if 'contact' in description_lower or 'person' in description_lower:
            required_inputs.append('Contact person/information')
        if 'file' in description_lower or 'document' in description_lower:
            required_inputs.append('File/document references')
        if 'budget' in description_lower or 'cost' in description_lower:
            required_inputs.append('Budget/cost information')
        if 'approval' in description_lower:
            required_inputs.append('Approval authority')

        # Add general inputs
        required_inputs.extend(['Success criteria', 'Constraints', 'Priority level'])

        return required_inputs

    def _suggest_approach(self, task_description: str) -> str:
        """Suggest an approach based on task description"""
        description_lower = task_description.lower()

        if 'schedule' in description_lower or 'meeting' in description_lower:
            return "Propose scheduling approach with calendar integration and availability checking"
        elif 'email' in description_lower:
            return "Suggest email drafting with template selection and recipient verification"
        elif 'report' in description_lower or 'analyze' in description_lower:
            return "Recommend data gathering, analysis, and visualization approach"
        elif 'approval' in description_lower:
            return "Propose approval workflow with stakeholder identification and process documentation"
        else:
            return "Suggest breaking down the task into manageable steps with clear milestones and checkpoints"

    def update_collaboration(self, collaboration_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an ongoing collaboration with new information

        Args:
            collaboration_id: ID of the collaboration to update
            updates: Dictionary with updates

        Returns:
            True if update was successful, False otherwise
        """
        for i, task in enumerate(self.active_tasks):
            if task['id'] == collaboration_id:
                # Update the task with new information
                for key, value in updates.items():
                    self.active_tasks[i][key] = value

                # Update the status based on progress
                if 'progress' in updates:
                    if updates['progress'] >= 1.0:
                        self.active_tasks[i]['status'] = 'completed'
                    elif updates['progress'] > 0:
                        self.active_tasks[i]['status'] = 'in_progress'

                log_activity("COLLABORATION_UPDATED", f"Updated collaboration {collaboration_id}", "obsidian_vault")
                return True

        return False

    def get_collaboration_status(self, collaboration_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of an ongoing collaboration

        Args:
            collaboration_id: ID of the collaboration

        Returns:
            Collaboration status information or None if not found
        """
        for task in self.active_tasks:
            if task['id'] == collaboration_id:
                return {
                    'id': task['id'],
                    'status': task['status'],
                    'progress': task['progress'],
                    'steps_completed': len([s for s in task.get('steps', []) if s.get('completed', False)]),
                    'total_steps': len(task.get('steps', [])),
                    'estimated_completion': task.get('estimated_completion'),
                    'last_update': task.get('last_update', datetime.now()),
                    'required_inputs': task.get('required_inputs', []),
                    'suggested_approach': task.get('suggested_approach', '')
                }

        return None

    def complete_collaboration(self, collaboration_id: str, final_output: str = "") -> bool:
        """
        Complete a collaboration and archive it

        Args:
            collaboration_id: ID of the collaboration to complete
            final_output: Final output of the collaboration

        Returns:
            True if completion was successful, False otherwise
        """
        for i, task in enumerate(self.active_tasks):
            if task['id'] == collaboration_id:
                # Mark as completed
                self.active_tasks[i]['status'] = 'completed'
                self.active_tasks[i]['completed_at'] = datetime.now()
                self.active_tasks[i]['final_output'] = final_output
                self.active_tasks[i]['progress'] = 1.0

                # Move to completed tasks (in a real system, this would be stored separately)
                completed_task = self.active_tasks.pop(i)

                log_activity("COLLABORATION_COMPLETED", f"Completed collaboration {collaboration_id}", "obsidian_vault")
                return True

        return False

    def request_human_input(self, request_type: str, context: str = "", options: List[str] = None) -> Dict[str, Any]:
        """
        Request specific input from the human collaborator

        Args:
            request_type: Type of input requested
            context: Context for the request
            options: Optional list of choices

        Returns:
            Request details for the human
        """
        request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        request = {
            'id': request_id,
            'type': request_type,
            'context': context,
            'options': options or [],
            'timestamp': datetime.now(),
            'status': 'pending',
            'urgency': 'normal'
        }

        # Add to pending requests
        self.pending_decisions.append(request)

        response = {
            'request_id': request_id,
            'request_type': request_type,
            'message': self._compose_request_message(request_type, context, options),
            'options': options or [],
            'context': context,
            'is_choice_required': bool(options)
        }

        log_activity("INPUT_REQUESTED", f"Requested human input: {request_type}", "obsidian_vault")
        return response

    def _compose_request_message(self, request_type: str, context: str, options: List[str]) -> str:
        """Compose an appropriate message for the human input request"""
        if request_type == "approval":
            return f"I need your approval for: {context}. Please confirm or deny."
        elif request_type == "clarification":
            return f"I need clarification on: {context}. Could you provide more details?"
        elif request_type == "choice":
            if options:
                return f"Please choose from the following options for '{context}': {', '.join(options)}"
            else:
                return f"What would you prefer for: {context}?"
        elif request_type == "feedback":
            return f"How would you rate the following: {context}? Please provide feedback."
        elif request_type == "verification":
            return f"Please verify: {context}. Is this correct?"
        else:
            return f"I need your input on: {context}. What should I do?"

    def process_human_response(self, request_id: str, response: Union[str, int]) -> Dict[str, Any]:
        """
        Process a response from the human collaborator

        Args:
            request_id: ID of the original request
            response: Response from the human

        Returns:
            Processing result
        """
        for i, request in enumerate(self.pending_decisions):
            if request['id'] == request_id:
                # Process the response based on request type
                result = self._handle_response(request, response)

                # Mark request as completed
                self.pending_decisions[i]['status'] = 'completed'
                self.pending_decisions[i]['response'] = response
                self.pending_decisions[i]['completed_at'] = datetime.now()

                # Remove from pending if processed
                completed_request = self.pending_decisions.pop(i)

                return {
                    'status': 'processed',
                    'request_id': request_id,
                    'response': response,
                    'action_taken': result,
                    'success': True
                }

        return {
            'status': 'error',
            'request_id': request_id,
            'error': 'Request not found',
            'success': False
        }

    def _handle_response(self, request: Dict[str, Any], response: Union[str, int]) -> str:
        """Handle the human response based on request type"""
        req_type = request['type']

        if req_type == "approval":
            if str(response).lower() in ['yes', 'approve', 'ok', '1', 'true', 'confirm']:
                return "Action approved, proceeding with execution"
            else:
                return "Action denied, cancelling operation"
        elif req_type == "clarification":
            return f"Received clarification: {response}, continuing with task"
        elif req_type == "choice":
            try:
                choice_idx = int(response)
                if 0 <= choice_idx < len(request['options']):
                    return f"Selected option: {request['options'][choice_idx]}"
                else:
                    return f"Invalid option index, using default"
            except ValueError:
                # Response might be the actual option text
                if str(response) in request['options']:
                    return f"Selected option: {response}"
                else:
                    return f"Invalid option: {response}, using default"
        elif req_type == "feedback":
            return f"Received feedback: {response}, incorporating into process"
        elif req_type == "verification":
            if str(response).lower() in ['yes', 'correct', 'ok', 'true']:
                return "Verification confirmed, proceeding"
            else:
                return "Verification failed, need correction"
        else:
            return f"Processed response: {response} for {req_type} request"

    def provide_explanation(self, action_taken: str, reasoning: str) -> str:
        """
        Provide explanation for actions taken

        Args:
            action_taken: Action that was performed
            reasoning: Reasoning behind the action

        Returns:
            Formatted explanation
        """
        explanation = f"""
        Action: {action_taken}

        Rationale: {reasoning}

        Impact: This action was taken to optimize the task completion and align with your preferences and requirements.

        Alternative approaches considered:
        - Manual execution (but AI automation is more efficient)
        - Different timing (but current timing optimizes dependencies)
        - Alternative methods (but this approach best fits your context)

        Confidence in decision: High
        """

        log_activity("EXPLANATION_PROVIDED", f"Explained action: {action_taken[:50]}...", "obsidian_vault")
        return explanation.strip()

    def summarize_interaction(self, user_id: str, time_window: timedelta = timedelta(hours=1)) -> Dict[str, Any]:
        """
        Summarize recent interactions with a user

        Args:
            user_id: ID of the user
            time_window: Time window for summary

        Returns:
            Interaction summary
        """
        start_time = datetime.now() - time_window

        user_interactions = [
            interaction for interaction in self.conversation_history
            if interaction['user_id'] == user_id and interaction['timestamp'] >= start_time
        ]

        if not user_interactions:
            return {
                'user_id': user_id,
                'time_window': time_window.total_seconds() / 3600,  # Hours
                'interaction_count': 0,
                'summary': 'No recent interactions found',
                'emotions': {},
                'topics': []
            }

        # Analyze interactions
        emotions = {}
        topics = []
        styles_used = []

        for interaction in user_interactions:
            emotion = interaction['emotion']
            emotions[emotion] = emotions.get(emotion, 0) + 1

            style = interaction['style']
            styles_used.append(style)

            # Extract potential topics (simplified)
            text = interaction['user_input'] + ' ' + interaction['ai_response']
            words = text.lower().split()
            topics.extend([word for word in words if len(word) > 4 and word.isalpha()])

        # Get most common topics
        topic_counts = {}
        for topic in topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        most_common_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        summary = {
            'user_id': user_id,
            'time_window': time_window.total_seconds() / 3600,  # Hours
            'interaction_count': len(user_interactions),
            'average_response_time': 'N/A',  # Would need timing data
            'dominant_emotion': max(emotions, key=emotions.get) if emotions else 'neutral',
            'emotions': emotions,
            'most_common_communication_style': max(set(styles_used), key=styles_used.count) if styles_used else 'formal',
            'topics_discussed': [topic for topic, count in most_common_topics],
            'summary': f"Engaged in {len(user_interactions)} interactions with predominantly {max(emotions, key=emotions.get) if emotions else 'neutral'} sentiment"
        }

        return summary

    def adapt_to_user_feedback(self, user_id: str, feedback: str, rating: int = 5) -> Dict[str, Any]:
        """
        Adapt behavior based on user feedback

        Args:
            user_id: ID of the user
            feedback: Feedback text
            rating: Rating from 1-10

        Returns:
            Adaptation results
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}

        # Update user profile with feedback
        if 'feedback_history' not in self.user_profiles[user_id]:
            self.user_profiles[user_id]['feedback_history'] = []

        self.user_profiles[user_id]['feedback_history'].append({
            'feedback': feedback,
            'rating': rating,
            'timestamp': datetime.now()
        })

        # Analyze feedback for adaptation
        feedback_lower = feedback.lower()

        adaptations = {
            'communication_style_changed': False,
            'interaction_mode_changed': False,
            'behavior_adjustments': [],
            'confidence_in_changes': 0.0
        }

        # Adjust communication style based on feedback
        if 'too formal' in feedback_lower:
            self.user_profiles[user_id]['communication_style'] = CommunicationStyle.CASUAL.value
            adaptations['communication_style_changed'] = True
            adaptations['behavior_adjustments'].append('Adjusted to more casual communication')
        elif 'too casual' in feedback_lower:
            self.user_profiles[user_id]['communication_style'] = CommunicationStyle.FORMAL.value
            adaptations['communication_style_changed'] = True
            adaptations['behavior_adjustments'].append('Adjusted to more formal communication')
        elif 'not detailed enough' in feedback_lower:
            self.user_profiles[user_id]['communication_style'] = CommunicationStyle.TECHNICAL.value
            adaptations['communication_style_changed'] = True
            adaptations['behavior_adjustments'].append('Providing more detailed responses')
        elif 'too technical' in feedback_lower:
            self.user_profiles[user_id]['communication_style'] = CommunicationStyle.NON_TECHNICAL.value
            adaptations['communication_style_changed'] = True
            adaptations['behavior_adjustments'].append('Using simpler language')

        # Adjust based on rating
        if rating <= 3:
            adaptations['interaction_mode_changed'] = True
            self.set_interaction_mode(InteractionMode.SUPERVISED, user_id)
            adaptations['behavior_adjustments'].append('Switched to supervised mode for better oversight')
        elif rating >= 8:
            # Could switch to more autonomous mode, but keeping assistive as default
            pass

        # Calculate confidence in adaptations
        adaptations['confidence_in_changes'] = min(1.0, len(adaptations['behavior_adjustments']) * 0.3 + (rating / 10.0) * 0.5)

        log_activity("FEEDBACK_PROCESSED", f"Processed feedback from user {user_id}, made {len(adaptations['behavior_adjustments'])} adjustments", "obsidian_vault")
        return adaptations


# Example usage and testing
if __name__ == "__main__":
    print("Testing Collaboration Engine...")

    # Initialize collaboration engine
    collaboration_engine = CollaborationEngine()

    # Test emotion detection
    print("\n1. Testing Emotion Detection:")
    test_inputs = [
        "This is great! I love this feature.",
        "This is terrible and I hate it.",
        "I'm not sure how this works, can you explain?",
        "Why isn't this working? This is broken!",
        "Okay, that makes sense."
    ]

    for inp in test_inputs:
        emotion = collaboration_engine.analyze_user_emotion(inp)
        style = collaboration_engine.adapt_communication_style("test_user", emotion)
        print(f"'{inp[:30]}...' -> {emotion.value}, Style: {style.value}")

    # Test response generation
    print("\n2. Testing Response Generation:")
    response = collaboration_engine.generate_response(
        "Please schedule a meeting with the marketing team for next Tuesday",
        "test_user_001"
    )
    print(f"Response: {response['response_text']}")
    print(f"Emotion: {response['emotion_detected']}, Style: {response['communication_style']}")
    print(f"Suggestions: {response['suggested_next_actions']}")

    # Test collaboration initiation
    print("\n3. Testing Collaboration Initiation:")
    collaboration = collaboration_engine.initiate_collaboration(
        "Schedule a meeting with the marketing team for next Tuesday",
        "test_user_001"
    )
    print(f"Collaboration ID: {collaboration['collaboration_id']}")
    print(f"Required inputs: {collaboration['required_inputs']}")
    print(f"Suggested approach: {collaboration['suggested_approach']}")

    # Test setting interaction mode
    print("\n4. Testing Interaction Mode:")
    collaboration_engine.set_interaction_mode(InteractionMode.COLLABORATIVE, "test_user_001")
    print(f"Current mode: {collaboration_engine.current_mode.value}")

    # Test requesting human input
    print("\n5. Testing Human Input Request:")
    request = collaboration_engine.request_human_input(
        "approval",
        "Sending email to all marketing team members about the meeting",
        ["Approve", "Modify", "Cancel"]
    )
    print(f"Request ID: {request['request_id']}")
    print(f"Message: {request['message']}")
    print(f"Options: {request['options']}")

    # Test processing human response
    print("\n6. Testing Response Processing:")
    result = collaboration_engine.process_human_response(request['request_id'], "Approve")
    print(f"Processing result: {result['action_taken']}")

    # Test providing explanation
    print("\n7. Testing Explanation:")
    explanation = collaboration_engine.provide_explanation(
        "Scheduled meeting for Tuesday",
        "Based on user request and calendar availability, Tuesday at 10AM was optimal"
    )
    print(f"Explanation: {explanation[:100]}...")

    # Test adaptation to feedback
    print("\n8. Testing Feedback Adaptation:")
    adaptations = collaboration_engine.adapt_to_user_feedback(
        "test_user_001",
        "The communication is too formal, please be more casual",
        rating=4
    )
    print(f"Adaptations made: {adaptations['behavior_adjustments']}")
    print(f"Style changed: {adaptations['communication_style_changed']}")

    # Test interaction summary
    print("\n9. Testing Interaction Summary:")
    summary = collaboration_engine.summarize_interaction("test_user_001", timedelta(minutes=30))
    print(f"Interactions: {summary['interaction_count']}")
    print(f"Dominant emotion: {summary['dominant_emotion']}")
    print(f"Topics: {summary['topics_discussed'][:3]}")

    print("\nCollaboration Engine tests completed!")
"""
Adaptive Learning Service for Silver Tier Personal AI Employee System
Provides adaptive learning and behavioral modeling capabilities
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import math
from dataclasses import dataclass
from enum import Enum

from .database import UserPreference, InteractionLog
from .preference_service import UserPreferenceService
from .interaction_service import InteractionService
from ..utils.logger import log_activity


class LearningEventType(Enum):
    TASK_COMPLETED = "task_completed"
    APPROVAL_GRANTED = "approval_granted"
    CORRECTION_MADE = "correction_made"
    FEEDBACK_PROVIDED = "feedback_provided"
    PATTERN_RECOGNIZED = "pattern_recognized"
    PREFERENCE_ADAPTED = "preference_adapted"


@dataclass
class LearningEvent:
    """Data class for learning events"""
    user_id: str
    event_type: LearningEventType
    context: Dict[str, Any]
    outcome: str  # positive, negative, neutral
    timestamp: datetime
    confidence: float  # 0-1


class AdaptiveLearningService:
    """
    Service for adaptive learning and behavioral modeling in Silver Tier
    """

    def __init__(self, db_session):
        self.db = db_session
        self.preference_service = UserPreferenceService(db_session)
        self.interaction_service = InteractionService(db_session)
        self.learning_events = []

    def process_interaction_learning(self, user_id: str, interaction: InteractionLog) -> bool:
        """
        Process an interaction to extract learning and update preferences

        Args:
            user_id: User identifier
            interaction: Interaction log entry

        Returns:
            True if learning was applied, False otherwise
        """
        try:
            # Determine if this interaction provides learning opportunity
            if interaction.learning_applied:
                return False  # Already processed

            # Update preference based on outcome
            if interaction.outcome == "positive":
                self._reinforce_positive_behavior(user_id, interaction)
            elif interaction.outcome == "negative":
                self._adjust_for_negative_outcome(user_id, interaction)

            # Mark the interaction as having learning applied
            self.interaction_service.mark_learning_applied(interaction.id)

            log_activity("LEARNING_PROCESSED",
                       f"Learning extracted from interaction {interaction.id} for user {user_id}",
                       "obsidian_vault")

            return True
        except Exception as e:
            log_activity("LEARNING_ERROR",
                       f"Error processing learning from interaction {interaction.id}: {str(e)}",
                       "obsidian_vault")
            return False

    def _reinforce_positive_behavior(self, user_id: str, interaction: InteractionLog):
        """
        Reinforce behaviors that led to positive outcomes
        """
        # If this was a correction, update the preference that caused the need for correction
        if interaction.interaction_type == "correction":
            # Identify the preference that might need adjustment
            # For example, if the AI categorized incorrectly, adjust categorization preferences
            self._adjust_categorization_preferences(user_id, interaction)

        # If this was feedback, incorporate it into preferences
        elif interaction.interaction_type == "feedback" and interaction.feedback_text:
            self._incorporate_feedback(user_id, interaction)

        # If this was approval, update approval-related preferences
        elif interaction.interaction_type == "approval":
            # Increase confidence in approval decision-making
            approval_pref = self.preference_service.get_preference(user_id, "approval_threshold")
            if approval_pref:
                current_value = self.preference_service.deserialize_preference_value(approval_pref)
                if current_value and isinstance(current_value, dict):
                    # Slightly decrease threshold (more permissive) if outcome was positive
                    current_amount = current_value.get("amount", 100)
                    new_amount = max(50, current_amount * 0.95)  # Reduce by 5%

                    self.preference_service.update_preference_value(
                        user_id, "approval_threshold", {
                            "amount": new_amount,
                            "currency": current_value.get("currency", "USD"),
                            "requires_approval": True
                        }
                    )
                    self.preference_service.update_effectiveness_score(
                        user_id, "approval_threshold", min(1.0, approval_pref.effectiveness_score + 0.05)
                    )

    def _adjust_for_negative_outcome(self, user_id: str, interaction: InteractionLog):
        """
        Adjust preferences based on negative outcomes
        """
        # If this was a correction, be more conservative in similar situations
        if interaction.interaction_type == "correction":
            # Make the AI more cautious in similar situations
            self._increase_caution(user_id, interaction)

        # If this was feedback indicating dissatisfaction
        elif interaction.interaction_type == "feedback" and interaction.feedback_text:
            self._adjust_for_feedback(user_id, interaction)

        # If this was an approval that led to negative outcome
        elif interaction.interaction_type == "approval":
            approval_pref = self.preference_service.get_preference(user_id, "approval_threshold")
            if approval_pref:
                current_value = self.preference_service.deserialize_preference_value(approval_pref)
                if current_value and isinstance(current_value, dict):
                    # Increase threshold (more conservative) if outcome was negative
                    current_amount = current_value.get("amount", 100)
                    new_amount = current_amount * 1.1  # Increase by 10%

                    self.preference_service.update_preference_value(
                        user_id, "approval_threshold", {
                            "amount": new_amount,
                            "currency": current_value.get("currency", "USD"),
                            "requires_approval": True
                        }
                    )
                    self.preference_service.update_effectiveness_score(
                        user_id, "approval_threshold", max(-1.0, approval_pref.effectiveness_score - 0.1)
                    )

    def _adjust_categorization_preferences(self, user_id: str, interaction: InteractionLog):
        """
        Adjust categorization preferences based on correction
        """
        # Extract context to understand what category was corrected
        context = self.interaction_service.deserialize_context_snapshot(interaction)
        if context and "expected_category" in context and "actual_category" in context:
            expected = context["expected_category"]
            actual = context["actual_category"]

            # Update the preference for this specific case
            category_pref_key = f"category_preference_{actual}_to_{expected}"
            existing_pref = self.preference_service.get_preference(user_id, category_pref_key)

            if existing_pref:
                # Update existing preference
                current_confidence = existing_pref.confidence_level
                new_confidence = min(1.0, current_confidence + 0.1)  # Increase confidence

                self.preference_service.update_preference_value(
                    user_id, category_pref_key, {"correct_mapping": True}
                )
                self.preference_service.update_effectiveness_score(
                    user_id, category_pref_key, min(1.0, existing_pref.effectiveness_score + 0.1)
                )
            else:
                # Create new preference based on correction
                self.preference_service.create_preference(
                    user_id=user_id,
                    preference_key=category_pref_key,
                    preference_value={"correct_mapping": True},
                    preference_type="behavioral",
                    confidence_level=0.7
                )

    def _incorporate_feedback(self, user_id: str, interaction: InteractionLog):
        """
        Incorporate feedback into preferences
        """
        feedback_text = interaction.feedback_text.lower()

        # Check for specific feedback patterns
        if "too formal" in feedback_text or "too stiff" in feedback_text:
            # Adjust communication style to be less formal
            comm_pref = self.preference_service.get_preference(user_id, "email_response_style")
            if comm_pref:
                current_style = self.preference_service.deserialize_preference_value(comm_pref)
                if current_style and isinstance(current_style, dict):
                    current_style["tone"] = "friendly"
                    self.preference_service.update_preference_value(
                        user_id, "email_response_style", current_style
                    )
                    self.preference_service.update_effectiveness_score(
                        user_id, "email_response_style",
                        min(1.0, comm_pref.effectiveness_score + 0.05)
                    )

        elif "too casual" in feedback_text or "unprofessional" in feedback_text:
            # Adjust communication style to be more formal
            comm_pref = self.preference_service.get_preference(user_id, "email_response_style")
            if comm_pref:
                current_style = self.preference_service.deserialize_preference_value(comm_pref)
                if current_style and isinstance(current_style, dict):
                    current_style["tone"] = "professional"
                    self.preference_service.update_preference_value(
                        user_id, "email_response_style", current_style
                    )
                    self.preference_service.update_effectiveness_score(
                        user_id, "email_response_style",
                        min(1.0, comm_pref.effectiveness_score + 0.05)
                    )

    def _adjust_for_feedback(self, user_id: str, interaction: InteractionLog):
        """
        Adjust preferences based on negative feedback
        """
        feedback_text = interaction.feedback_text.lower()

        if "slower" in feedback_text or "take more time" in feedback_text:
            # Adjust to be more thorough
            speed_pref = self.preference_service.get_preference(user_id, "task_processing_speed")
            if speed_pref:
                current_speed = self.preference_service.deserialize_preference_value(speed_pref)
                if current_speed and isinstance(current_speed, dict):
                    current_speed["approach"] = "thorough"
                    self.preference_service.update_preference_value(
                        user_id, "task_processing_speed", current_speed
                    )
                    self.preference_service.update_effectiveness_score(
                        user_id, "task_processing_speed",
                        max(-1.0, speed_pref.effectiveness_score - 0.05)
                    )

    def _increase_caution(self, user_id: str, interaction: InteractionLog):
        """
        Increase caution based on correction
        """
        # Increase confidence threshold for similar tasks
        caution_pref = self.preference_service.get_preference(user_id, "decision_confidence_threshold")
        if caution_pref:
            current_threshold = self.preference_service.deserialize_preference_value(caution_pref)
            if current_threshold and isinstance(current_threshold, dict):
                current_value = current_threshold.get("threshold", 0.7)
                new_value = min(0.95, current_value + 0.05)  # Increase threshold by 5%

                self.preference_service.update_preference_value(
                    user_id, "decision_confidence_threshold", {
                        "threshold": new_value,
                        "requires_human_review": True
                    }
                )
                self.preference_service.update_effectiveness_score(
                    user_id, "decision_confidence_threshold",
                    max(-1.0, caution_pref.effectiveness_score - 0.05)
                )

    def learn_from_user_behavior(self, user_id: str) -> bool:
        """
        Analyze user behavior patterns and update preferences accordingly

        Args:
            user_id: User identifier

        Returns:
            True if learning was applied, False otherwise
        """
        try:
            # Get recent interactions for the user
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_interactions = self.interaction_service.get_interactions_by_date_range(
                user_id, thirty_days_ago, datetime.utcnow()
            )

            if not recent_interactions:
                return False

            # Analyze patterns in the interactions
            pattern_analysis = self._analyze_behavioral_patterns(recent_interactions)

            # Update preferences based on patterns
            self._update_preferences_from_patterns(user_id, pattern_analysis)

            log_activity("BEHAVIOR_LEARNING",
                       f"Learned from {len(recent_interactions)} interactions for user {user_id}",
                       "obsidian_vault")

            return True
        except Exception as e:
            log_activity("BEHAVIOR_LEARNING_ERROR",
                       f"Error in behavior learning for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return False

    def _analyze_behavioral_patterns(self, interactions: List[InteractionLog]) -> Dict[str, Any]:
        """
        Analyze patterns in user interactions
        """
        patterns = {
            'response_time_preferences': {},
            'decision_making_style': {},
            'communication_preferences': {},
            'task_handling_patterns': {},
            'frequency_patterns': {}
        }

        if not interactions:
            return patterns

        # Analyze response time patterns
        approval_interactions = [i for i in interactions if i.interaction_type == "approval"]
        if approval_interactions:
            response_times = []
            for interaction in approval_interactions:
                # Calculate time between request and response if available
                # For now, we'll use a placeholder
                response_times.append(24)  # 24 hours average

            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                patterns['response_time_preferences'] = {
                    'average_response_time': avg_response_time,
                    'urgency_preference': 'standard' if avg_response_time > 24 else 'expedited'
                }

        # Analyze decision-making patterns
        approval_outcomes = [i for i in interactions if i.interaction_type == "approval"]
        if approval_outcomes:
            approvals = len([i for i in approval_outcomes if i.outcome == "positive"])
            total_approvals = len(approval_outcomes)
            approval_rate = approvals / total_approvals if total_approvals > 0 else 0

            patterns['decision_making_style'] = {
                'approval_rate': approval_rate,
                'risk_tolerance': 'high' if approval_rate > 0.8 else 'low' if approval_rate < 0.5 else 'medium'
            }

        # Analyze communication patterns
        feedback_interactions = [i for i in interactions if i.interaction_type == "feedback"]
        if feedback_interactions:
            feedback_texts = [i.feedback_text for i in feedback_interactions if i.feedback_text]
            patterns['communication_preferences'] = {
                'feedback_frequency': len(feedback_texts) / len(interactions),
                'positive_sentiment_ratio': len([ft for ft in feedback_texts if "good" in ft.lower() or "well" in ft.lower()]) / len(feedback_texts) if feedback_texts else 0
            }

        return patterns

    def _update_preferences_from_patterns(self, user_id: str, patterns: Dict[str, Any]):
        """
        Update user preferences based on identified patterns
        """
        # Update response time preferences
        if 'response_time_preferences' in patterns:
            resp_pref = patterns['response_time_preferences']
            existing_pref = self.preference_service.get_preference(user_id, "response_time_preference")

            if existing_pref:
                self.preference_service.update_preference_value(
                    user_id, "response_time_preference", resp_pref
                )
            else:
                self.preference_service.create_preference(
                    user_id=user_id,
                    preference_key="response_time_preference",
                    preference_value=resp_pref,
                    preference_type="operational",
                    confidence_level=0.6
                )

        # Update risk tolerance based on decision-making patterns
        if 'decision_making_style' in patterns:
            dm_style = patterns['decision_making_style']
            existing_pref = self.preference_service.get_preference(user_id, "risk_tolerance")

            if existing_pref:
                self.preference_service.update_preference_value(
                    user_id, "risk_tolerance", dm_style
                )
                # Adjust confidence based on consistency of pattern
                if dm_style['approval_rate'] > 0.7 or dm_style['approval_rate'] < 0.3:
                    # Strong pattern, increase confidence
                    self.preference_service.update_effectiveness_score(
                        user_id, "risk_tolerance",
                        min(1.0, existing_pref.effectiveness_score + 0.1)
                    )
            else:
                self.preference_service.create_preference(
                    user_id=user_id,
                    preference_key="risk_tolerance",
                    preference_value=dm_style,
                    preference_type="security",
                    confidence_level=0.5
                )

    def calculate_preference_confidence(self, user_id: str, preference_key: str) -> float:
        """
        Calculate the confidence level for a specific preference based on usage and outcomes

        Args:
            user_id: User identifier
            preference_key: Key of the preference

        Returns:
            Confidence level (0-1)
        """
        preference = self.preference_service.get_preference(user_id, preference_key)
        if not preference:
            return 0.0

        # Base confidence on usage count and effectiveness
        base_confidence = preference.confidence_level
        usage_factor = min(1.0, preference.usage_count / 100)  # Cap at 1.0 after 100 uses
        effectiveness_factor = (preference.effectiveness_score + 1) / 2  # Scale from -1:1 to 0:1

        # Combine factors
        combined_confidence = (
            base_confidence * 0.4 +  # Original confidence
            usage_factor * 0.3 +     # Usage factor
            effectiveness_factor * 0.3  # Effectiveness factor
        )

        return min(1.0, combined_confidence)

    def adapt_preference(self, user_id: str, preference_key: str, new_value: Any,
                        feedback_outcome: str = "neutral") -> bool:
        """
        Adapt a preference based on new information and feedback

        Args:
            user_id: User identifier
            preference_key: Key of the preference to adapt
            new_value: New value for the preference
            feedback_outcome: Outcome of previous use ("positive", "negative", "neutral")

        Returns:
            True if adaptation was successful, False otherwise
        """
        try:
            # Get the existing preference
            existing_preference = self.preference_service.get_preference(user_id, preference_key)

            if existing_preference:
                # Adjust confidence based on feedback outcome
                current_confidence = existing_preference.confidence_level
                current_effectiveness = existing_preference.effectiveness_score

                if feedback_outcome == "positive":
                    # Increase confidence and effectiveness
                    new_confidence = min(1.0, current_confidence + 0.05)
                    new_effectiveness = min(1.0, current_effectiveness + 0.1)
                elif feedback_outcome == "negative":
                    # Decrease confidence and effectiveness
                    new_confidence = max(0.1, current_confidence - 0.1)
                    new_effectiveness = max(-1.0, current_effectiveness - 0.2)
                else:
                    # Neutral feedback, slight adjustment
                    new_confidence = current_confidence
                    new_effectiveness = current_effectiveness

                # Update the preference value
                self.preference_service.update_preference_value(user_id, preference_key, new_value)

                # Update effectiveness score separately
                self.preference_service.update_effectiveness_score(
                    user_id, preference_key, new_effectiveness
                )

                # Update confidence in the preference record
                existing_preference.confidence_level = new_confidence
                existing_preference.updated_at = datetime.utcnow()
                self.db.commit()

                log_activity("PREFERENCE_ADAPTED",
                           f"Adapted preference {preference_key} for user {user_id}",
                           "obsidian_vault")

                return True
            else:
                # Create new preference
                self.preference_service.create_preference(
                    user_id=user_id,
                    preference_key=preference_key,
                    preference_value=new_value,
                    confidence_level=0.5 if feedback_outcome == "neutral" else 0.7 if feedback_outcome == "positive" else 0.3
                )

                log_activity("PREFERENCE_CREATED",
                           f"Created new preference {preference_key} for user {user_id}",
                           "obsidian_vault")

                return True

        except Exception as e:
            log_activity("PREFERENCE_ADAPTATION_ERROR",
                       f"Error adapting preference {preference_key} for user {user_id}: {str(e)}",
                       "obsidian_vault")
            return False

    def get_learning_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get a summary of learning for a user

        Args:
            user_id: User identifier

        Returns:
            Dictionary with learning summary
        """
        summary = {
            'preferences_learned': 0,
            'interactions_processed': 0,
            'adaptation_count': 0,
            'learning_effectiveness': 0.0,
            'recent_improvements': [],
            'suggested_learning_targets': []
        }

        # Count preferences
        preferences = self.preference_service.get_preferences_by_user(user_id)
        summary['preferences_learned'] = len(preferences)

        # Count interactions
        interactions = self.interaction_service.get_interactions_by_user(user_id)
        summary['interactions_processed'] = len(interactions)

        # Count applied learning
        applied_interactions = self.interaction_service.get_unapplied_learning_interactions(user_id)
        summary['adaptation_count'] = len(interactions) - len(applied_interactions)

        # Calculate learning effectiveness
        if preferences:
            total_effectiveness = sum(p.effectiveness_score for p in preferences)
            avg_effectiveness = total_effectiveness / len(preferences) if preferences else 0
            summary['learning_effectiveness'] = (avg_effectiveness + 1) / 2  # Scale from -1:1 to 0:1

        # Add recent improvements
        if interactions:
            recent_positive = [i for i in interactions[-5:] if i.outcome == "positive"]
            for interaction in recent_positive:
                summary['recent_improvements'].append({
                    'type': interaction.interaction_type,
                    'date': interaction.timestamp.isoformat(),
                    'description': f"Positive {interaction.interaction_type} interaction"
                })

        # Suggest learning targets
        if not preferences:
            summary['suggested_learning_targets'].extend([
                "Communication style preferences",
                "Task prioritization rules",
                "Approval threshold settings"
            ])
        else:
            # Suggest areas with low confidence
            low_confidence_prefs = [p for p in preferences if p.confidence_level < 0.5]
            for pref in low_confidence_prefs[:3]:  # Limit to top 3
                summary['suggested_learning_targets'].append(
                    f"Improve confidence in '{pref.preference_key}' preference"
                )

        return summary

    def apply_learning_to_task_processing(self, user_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply learned preferences to task processing

        Args:
            user_id: User identifier
            task_data: Raw task data

        Returns:
            Modified task data incorporating learned preferences
        """
        # Get all preferences for the user
        preferences = self.preference_service.get_preferences_by_user(user_id)

        # Create a copy of task data to modify
        processed_task = task_data.copy()

        # Apply various preferences to the task
        for preference in preferences:
            pref_value = self.preference_service.deserialize_preference_value(preference)

            if preference.preference_key == "default_task_priority":
                if "priority" not in processed_task or processed_task["priority"] == "medium":
                    if isinstance(pref_value, dict) and "value" in pref_value:
                        processed_task["priority"] = pref_value["value"]
                    elif isinstance(pref_value, str):
                        processed_task["priority"] = pref_value

            elif preference.preference_key == "default_task_category":
                if "category" not in processed_task:
                    if isinstance(pref_value, dict) and "value" in pref_value:
                        processed_task["category"] = pref_value["value"]
                    elif isinstance(pref_value, str):
                        processed_task["category"] = pref_value

            elif preference.preference_key == "decision_confidence_threshold":
                if isinstance(pref_value, dict):
                    threshold = pref_value.get("threshold", 0.7)
                    if "confidence_score" in processed_task and processed_task["confidence_score"] < threshold:
                        processed_task["requires_approval"] = True

            elif preference.preference_key == "email_response_style":
                if isinstance(pref_value, dict):
                    style_info = pref_value
                    processed_task["communication_style"] = style_info

        # Apply communication preferences if it's an email task
        if processed_task.get("category") == "email":
            comm_pref = self.preference_service.get_preference(user_id, "email_response_style")
            if comm_pref:
                style = self.preference_service.deserialize_preference_value(comm_pref)
                if style and isinstance(style, dict):
                    processed_task["email_style"] = style

        # Apply risk tolerance preferences
        risk_pref = self.preference_service.get_preference(user_id, "risk_tolerance")
        if risk_pref and processed_task.get("requires_approval") is not False:
            risk_tolerance = self.preference_service.deserialize_preference_value(risk_pref)
            if risk_tolerance and isinstance(risk_tolerance, dict):
                tolerance = risk_tolerance.get("risk_tolerance", "medium")
                if tolerance == "low" and "requires_approval" not in processed_task:
                    processed_task["requires_approval"] = True

        log_activity("LEARNING_APPLIED",
                   f"Applied learning to task processing for user {user_id}",
                   "obsidian_vault")

        return processed_task

    def train_on_batch_interactions(self, user_id: str, interactions: List[InteractionLog]) -> Dict[str, int]:
        """
        Train the learning model on a batch of interactions

        Args:
            user_id: User identifier
            interactions: List of interaction logs to learn from

        Returns:
            Dictionary with training results
        """
        results = {
            'processed': 0,
            'learned': 0,
            'errors': 0
        }

        for interaction in interactions:
            try:
                success = self.process_interaction_learning(user_id, interaction)
                results['processed'] += 1
                if success:
                    results['learned'] += 1
            except Exception as e:
                results['errors'] += 1
                log_activity("BATCH_TRAINING_ERROR",
                           f"Error processing interaction {interaction.id}: {str(e)}",
                           "obsidian_vault")

        log_activity("BATCH_TRAINING_COMPLETE",
                   f"Trained on {results['processed']} interactions for user {user_id} ({results['learned']} learned)",
                   "obsidian_vault")

        return results
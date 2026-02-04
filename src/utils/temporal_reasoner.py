"""
Temporal Reasoning Engine
NEW: Temporal reasoning and causality manipulation for Diamond Tier
Implements advanced temporal logic, causality analysis, and time manipulation capabilities.
"""

import asyncio
import json
import logging
import math
import random
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

import numpy as np
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class TemporalEvent(BaseModel):
    """
    Represents an event in temporal reasoning
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)
    perceived_time: Optional[datetime] = None  # Time as perceived by consciousness
    temporal_context: str = "present"  # 'past', 'present', 'future', 'eternal', 'timeless'
    causality_chain_id: Optional[str] = None
    cause_events: List[str] = Field(default_factory=list)  # IDs of causal events
    effect_events: List[str] = Field(default_factory=list)  # IDs of events caused
    temporal_distance: Optional[timedelta] = None  # Distance from reference time
    causality_strength: float = Field(ge=0.0, le=10.0, default=5.0)
    temporal_directionality: str = "forward"  # 'forward', 'backward', 'bidirectional', 'nonlinear'
    counterfactual_scenario: Optional[Dict[str, Any]] = None
    temporal_dependency_map: Dict[str, Any] = Field(default_factory=dict)
    paradox_indicators: List[str] = Field(default_factory=list)
    temporal_consistency_score: float = Field(ge=0.0, le=10.0, default=8.0)
    closed_timelike_curve: bool = False
    temporal_influence_radius: Optional[timedelta] = None
    causality_confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    retrocausal_indicators: List[str] = Field(default_factory=list)
    temporal_branch_probability: Dict[str, float] = Field(default_factory=dict)
    causality_alternatives: List[Dict[str, Any]] = Field(default_factory=list)
    temporal_paradox_resolution: Optional[Dict[str, Any]] = None
    temporal_stability_index: float = Field(ge=0.0, le=10.0, default=7.0)
    causality_complexity: str = "simple"  # 'simple', 'moderate', 'complex', 'paradoxical', 'intractable'
    temporal_awareness_context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TemporalCausalityChain(BaseModel):
    """
    Represents a chain of causally connected events
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    chain_name: str
    start_event_id: str
    end_event_id: str
    events_in_chain: List[str] = Field(default_factory=list)
    causality_strength: float = Field(ge=0.0, le=10.0, default=5.0)
    temporal_direction: str = "forward"  # 'forward', 'backward', 'bidirectional'
    duration: Optional[timedelta] = None
    complexity: str = "moderate"  # 'simple', 'moderate', 'complex', 'paradoxical'
    stability: float = Field(ge=0.0, le=10.0, default=7.0)
    paradox_risk: float = Field(ge=0.0, le=10.0, default=2.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TemporalLogicFramework:
    """
    Framework for temporal reasoning and logic operations
    """

    def __init__(self):
        self.temporal_operators = {
            'always': '[]',
            'eventually': '<>',
            'until': 'U',
            'next': 'X',
            'since': 'S',
            'triggered': 'T'
        }

    def evaluate_temporal_formula(self, formula: str, timeline: List[TemporalEvent]) -> bool:
        """
        Evaluate a temporal logic formula against a timeline of events
        """
        # Parse and evaluate the formula
        # This is a simplified implementation - in practice, this would be much more complex
        if 'always' in formula.lower():
            # Check if a condition holds at all times
            condition = formula.replace('always', '').strip()
            return all(self.evaluate_condition(condition, event) for event in timeline)
        elif 'eventually' in formula.lower():
            # Check if a condition eventually holds
            condition = formula.replace('eventually', '').strip()
            return any(self.evaluate_condition(condition, event) for event in timeline)
        elif 'until' in formula.lower():
            # Check if one condition holds until another becomes true
            parts = formula.split('until')
            if len(parts) == 2:
                condition1, condition2 = parts[0].strip(), parts[1].strip()
                return self.evaluate_until(condition1, condition2, timeline)

        return False

    def evaluate_condition(self, condition: str, event: TemporalEvent) -> bool:
        """
        Evaluate a condition against an event
        """
        # Simplified condition evaluation
        condition_lower = condition.lower()

        if 'happened' in condition_lower:
            return True  # All events have happened
        elif 'caused' in condition_lower:
            return len(event.cause_events) > 0
        elif 'effect' in condition_lower:
            return len(event.effect_events) > 0

        return True  # Default to true

    def evaluate_until(self, condition1: str, condition2: str, timeline: List[TemporalEvent]) -> bool:
        """
        Evaluate an 'until' condition
        """
        # Check if condition1 holds until condition2 becomes true
        condition2_met = False
        for event in timeline:
            if self.evaluate_condition(condition2, event):
                condition2_met = True
                break
            if not self.evaluate_condition(condition1, event):
                return False

        return condition2_met


class CausalityAnalyzer:
    """
    Analyzes causal relationships between events
    """

    def __init__(self):
        self.causality_rules = []
        self.counterfactual_scenarios = []

    def analyze_causality(self, event_sequence: List[TemporalEvent]) -> Dict[str, Any]:
        """
        Analyze causality in a sequence of events
        """
        analysis = {
            'causal_chains': [],
            'direct_causes': [],
            'indirect_causes': [],
            'correlations': [],
            'causality_confidence_scores': {},
            'potential_confounding_factors': [],
            'causality_strength_matrix': [],
            'temporal_gap_analysis': {}
        }

        if len(event_sequence) < 2:
            return analysis

        # Analyze pairs of events
        for i in range(len(event_sequence)):
            current_event = event_sequence[i]

            for j in range(i + 1, len(event_sequence)):
                other_event = event_sequence[j]

                # Calculate temporal gap
                time_diff = abs((current_event.timestamp - other_event.timestamp).total_seconds())

                # Determine potential causality
                if time_diff < 3600:  # Within an hour
                    potential_causality = self.assess_potential_causality(current_event, other_event)

                    if potential_causality['confidence'] > 0.5:
                        analysis['direct_causes'].append({
                            'cause_event_id': current_event.id,
                            'effect_event_id': other_event.id,
                            'confidence': potential_causality['confidence'],
                            'strength': potential_causality['strength'],
                            'type': potential_causality['type']
                        })

                        analysis['causality_confidence_scores'][f"{current_event.id}->{other_event.id}"] = potential_causality['confidence']

        return analysis

    def assess_potential_causality(self, cause_event: TemporalEvent, effect_event: TemporalEvent) -> Dict[str, Any]:
        """
        Assess the potential causality between two events
        """
        # Calculate various factors for causality assessment
        temporal_proximity = self.calculate_temporal_proximity(cause_event, effect_event)
        precedence = self.check_precedence(cause_event, effect_event)
        correlation = self.calculate_correlation(cause_event, effect_event)

        # Combine factors to determine causality
        combined_score = (temporal_proximity + precedence + correlation) / 3.0

        return {
            'confidence': combined_score,
            'strength': min(10.0, combined_score * 10),
            'type': 'potential_causal_link',
            'temporal_proximity': temporal_proximity,
            'precedence_score': precedence,
            'correlation_score': correlation
        }

    def calculate_temporal_proximity(self, event1: TemporalEvent, event2: TemporalEvent) -> float:
        """
        Calculate temporal proximity score (0-1)
        """
        time_diff = abs((event1.timestamp - event2.timestamp).total_seconds())

        # Closer in time = higher proximity score
        # Using exponential decay: score = e^(-time_diff/tau) where tau is a scaling factor
        tau = 3600  # 1 hour scaling factor
        proximity_score = math.exp(-time_diff / tau)

        return min(1.0, proximity_score)

    def check_precedence(self, cause_event: TemporalEvent, effect_event: TemporalEvent) -> float:
        """
        Check if cause precedes effect (0-1)
        """
        if cause_event.timestamp < effect_event.timestamp:
            return 1.0
        else:
            # For retrocausal analysis, return a lower score
            return 0.3

    def calculate_correlation(self, event1: TemporalEvent, event2: TemporalEvent) -> float:
        """
        Calculate correlation between events (0-1)
        """
        # Simplified correlation calculation
        # In a real implementation, this would analyze the content and context of events
        if event1.event_type == event2.event_type:
            return 0.8
        elif 'caused' in event1.description.lower() and event2.event_type in event1.description.lower():
            return 0.9
        elif 'affects' in event1.description.lower() or 'affects' in event2.description.lower():
            return 0.7
        else:
            return 0.2


class CounterfactualReasoning:
    """
    Handles counterfactual reasoning and "what if" scenarios
    """

    def __init__(self):
        self.scenario_library = {}

    def generate_counterfactual_scenario(self, original_event: TemporalEvent,
                                       alternative_action: str) -> Dict[str, Any]:
        """
        Generate a counterfactual scenario based on an alternative action
        """
        scenario = {
            'original_event_id': original_event.id,
            'alternative_action': alternative_action,
            'hypothesized_outcomes': [],
            'probability_assessment': {},
            'causal_impact_analysis': {},
            'temporal_implications': {},
            'generated_at': datetime.now().isoformat()
        }

        # Generate possible outcomes based on the alternative action
        possible_outcomes = self.generate_possible_outcomes(alternative_action)
        scenario['hypothesized_outcomes'] = possible_outcomes

        # Assess probabilities
        for outcome in possible_outcomes:
            prob = self.assess_probability(outcome, original_event)
            scenario['probability_assessment'][outcome] = prob

        return scenario

    def generate_possible_outcomes(self, action: str) -> List[str]:
        """
        Generate possible outcomes for an action
        """
        outcomes = []

        if 'send' in action.lower():
            outcomes = [
                'email_delivered_successfully',
                'email_marked_as_spam',
                'recipient_replies_positively',
                'recipient_ignores_email'
            ]
        elif 'schedule' in action.lower():
            outcomes = [
                'appointment_confirmed',
                'appointment_rescheduled',
                'appointment_cancelled',
                'double_booking_occurred'
            ]
        elif 'analyze' in action.lower():
            outcomes = [
                'insight_gained',
                'data_interpreted_correctly',
                'pattern_recognized',
                'misinterpretation_occurred'
            ]
        else:
            outcomes = [
                'action_successful',
                'action_partially_successful',
                'action_failed',
                'unexpected_outcome_occurred'
            ]

        return outcomes

    def assess_probability(self, outcome: str, original_event: TemporalEvent) -> float:
        """
        Assess the probability of an outcome
        """
        # Simplified probability assessment
        base_prob = 0.5

        # Adjust based on outcome type
        if 'successful' in outcome:
            base_prob += 0.2
        elif 'failed' in outcome:
            base_prob -= 0.2
        elif 'positive' in outcome:
            base_prob += 0.15

        # Adjust based on historical patterns
        if original_event.event_type in ['routine_task', 'scheduled_event']:
            success_prob = 0.8
        elif original_event.event_type in ['complex_analysis', 'strategic_decision']:
            success_prob = 0.6
        else:
            success_prob = 0.7

        # Combine base probability with event-specific probability
        final_prob = (base_prob + success_prob) / 2.0
        return max(0.0, min(1.0, final_prob))


class TemporalParadoxDetector:
    """
    Detects and resolves temporal paradoxes
    """

    def __init__(self):
        self.known_paradoxes = []
        self.resolutions_applied = []

    def detect_paradox(self, event_timeline: List[TemporalEvent]) -> List[Dict[str, Any]]:
        """
        Detect potential paradoxes in a timeline
        """
        paradoxes = []

        # Check for causal loops
        for i, event in enumerate(event_timeline):
            # Look for events that might cause themselves
            if event.id in event.cause_events:
                paradoxes.append({
                    'type': 'causal_loop',
                    'event_id': event.id,
                    'description': f'Event {event.id} references itself as a cause',
                    'severity': 'high',
                    'timestamp': datetime.now().isoformat()
                })

            # Check for grandfather paradox patterns
            if 'prevent' in event.description.lower() and 'birth' in event.description.lower():
                paradoxes.append({
                    'type': 'grandfather_paradox',
                    'event_id': event.id,
                    'description': f'Event {event.id} describes preventing a birth',
                    'severity': 'critical',
                    'timestamp': datetime.now().isoformat()
                })

            # Check for information paradoxes
            if 'information' in event.description.lower() and 'future' in event.description.lower():
                paradoxes.append({
                    'type': 'information_paradox',
                    'event_id': event.id,
                    'description': f'Event {event.id} involves information from the future',
                    'severity': 'medium',
                    'timestamp': datetime.now().isoformat()
                })

        return paradoxes

    def resolve_paradox(self, paradox: Dict[str, Any], timeline: List[TemporalEvent]) -> Dict[str, Any]:
        """
        Attempt to resolve a detected paradox
        """
        resolution = {
            'paradox_id': paradox['event_id'],
            'resolution_strategy': '',
            'applied_fixes': [],
            'new_timeline': timeline.copy(),
            'resolution_confidence': 0.0,
            'side_effects': [],
            'resolved_at': datetime.now().isoformat()
        }

        paradox_type = paradox['type']

        if paradox_type == 'causal_loop':
            # Break the loop by removing self-reference
            for event in resolution['new_timeline']:
                if event.id == paradox['event_id']:
                    event.cause_events = [ce for ce in event.cause_events if ce != event.id]
                    resolution['applied_fixes'].append('removed_self_reference')
                    resolution['resolution_strategy'] = 'causal_break'
                    resolution['resolution_confidence'] = 0.9
                    break

        elif paradox_type == 'grandfather_paradox':
            # Create a parallel timeline or prevent the paradox-causing action
            resolution['resolution_strategy'] = 'timeline_divergence'
            resolution['applied_fixes'].append('prevent_paradox_action')
            resolution['resolution_confidence'] = 0.8
            resolution['side_effects'].append('timeline_divergence_created')

        elif paradox_type == 'information_paradox':
            # Restrict information flow or add uncertainty
            resolution['resolution_strategy'] = 'information_restriction'
            resolution['applied_fixes'].append('add_information_uncertainty')
            resolution['resolution_confidence'] = 0.7

        self.resolutions_applied.append(resolution)
        return resolution


class TemporalReasoningEngine:
    """
    Main engine for temporal reasoning and time manipulation
    """

    def __init__(self):
        self.temporal_logic = TemporalLogicFramework()
        self.causality_analyzer = CausalityAnalyzer()
        self.counterfactual_reasoner = CounterfactualReasoning()
        self.paradox_detector = TemporalParadoxDetector()
        self.events = {}
        self.causality_chains = {}

    def create_temporal_event(self, event_type: str, description: str,
                           timestamp: Optional[datetime] = None) -> TemporalEvent:
        """
        Create a new temporal event
        """
        if timestamp is None:
            timestamp = datetime.now()

        event = TemporalEvent(
            event_type=event_type,
            description=description,
            timestamp=timestamp
        )

        self.events[event.id] = event
        return event

    def analyze_temporal_sequence(self, event_ids: List[str]) -> Dict[str, Any]:
        """
        Analyze a sequence of events temporally
        """
        events = [self.events[eid] for eid in event_ids if eid in self.events]
        events.sort(key=lambda e: e.timestamp)  # Sort by chronological order

        analysis = {
            'chronological_sequence': [e.id for e in events],
            'causality_analysis': self.causality_analyzer.analyze_causality(events),
            'temporal_patterns': self.identify_temporal_patterns(events),
            'predictive_indicators': self.extract_predictive_indicators(events),
            'anomaly_detection': self.detect_temporal_anomalies(events),
            'paradox_check': self.paradox_detector.detect_paradox(events),
            'temporal_consistency_score': self.calculate_temporal_consistency(events)
        }

        return analysis

    def identify_temporal_patterns(self, events: List[TemporalEvent]) -> List[Dict[str, Any]]:
        """
        Identify temporal patterns in a sequence of events
        """
        patterns = []

        if len(events) < 2:
            return patterns

        # Look for periodic patterns
        time_intervals = []
        for i in range(1, len(events)):
            interval = (events[i].timestamp - events[i-1].timestamp).total_seconds()
            time_intervals.append(interval)

        if time_intervals:
            avg_interval = sum(time_intervals) / len(time_intervals)
            std_dev = (sum((x - avg_interval) ** 2 for x in time_intervals) / len(time_intervals)) ** 0.5

            if std_dev / avg_interval < 0.1:  # Low variation = periodic
                patterns.append({
                    'type': 'periodic_pattern',
                    'average_interval_seconds': avg_interval,
                    'regularity_score': 1.0 - (std_dev / avg_interval),
                    'events_involved': [e.id for e in events]
                })

        # Look for clustering patterns
        clusters = self.identify_temporal_clusters(events)
        for cluster in clusters:
            patterns.append({
                'type': 'temporal_cluster',
                'cluster_events': cluster['event_ids'],
                'time_window': cluster['time_window'],
                'density': cluster['density']
            })

        return patterns

    def identify_temporal_clusters(self, events: List[TemporalEvent],
                                window_minutes: int = 60) -> List[Dict[str, Any]]:
        """
        Identify clusters of events within time windows
        """
        clusters = []
        events_sorted = sorted(events, key=lambda e: e.timestamp)

        i = 0
        while i < len(events_sorted):
            cluster_start = events_sorted[i].timestamp
            cluster_end = cluster_start + timedelta(minutes=window_minutes)
            cluster_events = []

            j = i
            while j < len(events_sorted) and events_sorted[j].timestamp <= cluster_end:
                cluster_events.append(events_sorted[j])
                j += 1

            if len(cluster_events) > 1:  # Only consider clusters with multiple events
                clusters.append({
                    'event_ids': [e.id for e in cluster_events],
                    'time_window': f"{cluster_start.isoformat()} to {cluster_end.isoformat()}",
                    'density': len(cluster_events) / (window_minutes / 60.0),  # Events per hour
                    'center_time': cluster_start + (cluster_end - cluster_start) / 2
                })

            i = j if j > i else i + 1

        return clusters

    def extract_predictive_indicators(self, events: List[TemporalEvent]) -> List[Dict[str, Any]]:
        """
        Extract predictive indicators from temporal sequences
        """
        indicators = []

        # Look for leading indicators
        for i, event in enumerate(events[:-1]):  # All except the last
            for subsequent_event in events[i+1:]:
                time_diff = (subsequent_event.timestamp - event.timestamp).total_seconds()

                # If event often precedes another within a reasonable timeframe
                if time_diff < 3600 and event.event_type != subsequent_event.event_type:
                    indicators.append({
                        'leading_event': event.id,
                        'predicted_event': subsequent_event.id,
                        'typical_lead_time': time_diff,
                        'confidence': 0.7  # Simplified confidence
                    })

        return indicators

    def detect_temporal_anomalies(self, events: List[TemporalEvent]) -> List[Dict[str, Any]]:
        """
        Detect temporal anomalies in event sequences
        """
        anomalies = []

        if len(events) < 2:
            return anomalies

        # Look for out-of-sequence events (temporal anomalies)
        events_sorted_by_time = sorted(events, key=lambda e: e.timestamp)
        events_sorted_by_id = sorted(events, key=lambda e: e.id)  # Assuming ID correlates with creation order

        for i, (time_seq_event, id_seq_event) in enumerate(zip(events_sorted_by_time, events_sorted_by_id)):
            if time_seq_event.id != id_seq_event.id:
                anomalies.append({
                    'type': 'temporal_sequence_anomaly',
                    'event_id': time_seq_event.id,
                    'expected_position': i,
                    'actual_position': events.index(time_seq_event),
                    'description': 'Event appears at unexpected time relative to creation order'
                })

        return anomalies

    def calculate_temporal_consistency(self, events: List[TemporalEvent]) -> float:
        """
        Calculate temporal consistency score (0-10)
        """
        if len(events) < 2:
            return 10.0  # Perfect consistency with one event

        # Check for consistency in temporal ordering
        ordered_by_time = [e.id for e in sorted(events, key=lambda e: e.timestamp)]
        ordered_by_creation = [e.id for e in sorted(events, key=lambda e: e.created_at)]

        # Calculate consistency as the ratio of matching positions
        matches = sum(1 for a, b in zip(ordered_by_time, ordered_by_creation) if a == b)
        consistency_score = (matches / len(events)) * 10.0

        return consistency_score

    def perform_counterfactual_reasoning(self, event_id: str, alternative_action: str) -> Dict[str, Any]:
        """
        Perform counterfactual reasoning on an event
        """
        if event_id not in self.events:
            return {'error': 'Event not found'}

        original_event = self.events[event_id]
        scenario = self.counterfactual_reasoner.generate_counterfactual_scenario(
            original_event, alternative_action
        )

        return {
            'original_event': original_event.dict(),
            'counterfactual_scenario': scenario,
            'analysis_timestamp': datetime.now().isoformat()
        }

    def manipulate_temporal_flow(self, manipulation_type: str, target_event_id: str,
                               duration: timedelta = timedelta(minutes=1)) -> Dict[str, Any]:
        """
        Manipulate temporal flow (for simulation purposes)
        """
        result = {
            'manipulation_type': manipulation_type,
            'target_event_id': target_event_id,
            'duration': duration.total_seconds(),
            'status': 'initiated',
            'effects': [],
            'warnings': [],
            'manipulation_id': str(uuid4()),
            'timestamp': datetime.now().isoformat()
        }

        if manipulation_type == 'accelerate':
            result['effects'].append('Time flow accelerated around target event')
            result['warnings'].append('May affect causality chains')
        elif manipulation_type == 'decelerate':
            result['effects'].append('Time flow decelerated around target event')
            result['warnings'].append('May cause temporal pressure buildup')
        elif manipulation_type == 'reverse':
            result['effects'].append('Time flow reversed around target event')
            result['warnings'].extend(['High paradox risk', 'Requires paradox prevention'])
        elif manipulation_type == 'pause':
            result['effects'].append('Time flow paused around target event')
            result['warnings'].append('Temporal inertia may accumulate')
        elif manipulation_type == 'loop':
            result['effects'].append('Time loop created around target event')
            result['warnings'].extend(['Extreme paradox risk', 'Requires stable anchor'])
        elif manipulation_type == 'branch':
            result['effects'].append('Timeline branched from target event')
            result['warnings'].append('Monitor for timeline convergence issues')
        elif manipulation_type == 'merge':
            result['effects'].append('Parallel timelines merged at target event')
            result['warnings'].append('Reality consistency check required')

        result['status'] = 'completed_with_effects'
        return result

    def evaluate_temporal_query(self, query: str, context_events: List[str]) -> Dict[str, Any]:
        """
        Evaluate a temporal reasoning query
        """
        events = [self.events[eid] for eid in context_events if eid in self.events]

        # Parse the query to determine what temporal reasoning is needed
        query_lower = query.lower()

        if 'before' in query_lower or 'after' in query_lower or 'when' in query_lower:
            # Temporal relationship query
            return self.evaluate_temporal_relationships(query, events)
        elif 'cause' in query_lower or 'because' in query_lower or 'why' in query_lower:
            # Causality query
            return self.evaluate_causality_query(query, events)
        elif 'could have' in query_lower or 'if' in query_lower:
            # Counterfactual query
            return self.evaluate_counterfactual_query(query, events)
        elif 'will happen' in query_lower or 'predict' in query_lower:
            # Predictive query
            return self.evaluate_predictive_query(query, events)
        else:
            # General temporal analysis
            return self.analyze_temporal_sequence(context_events)

    def evaluate_temporal_relationships(self, query: str, events: List[TemporalEvent]) -> Dict[str, Any]:
        """
        Evaluate queries about temporal relationships
        """
        results = {
            'query': query,
            'relationships': [],
            'chronological_analysis': {},
            'temporal_logic_evaluation': {}
        }

        # Sort events chronologically
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        for i, event in enumerate(sorted_events):
            if i > 0:
                prev_event = sorted_events[i-1]
                results['relationships'].append({
                    'first_event': prev_event.id,
                    'second_event': event.id,
                    'time_difference': (event.timestamp - prev_event.timestamp).total_seconds(),
                    'relationship': 'before->after'
                })

        results['chronological_analysis'] = {
            'earliest_event': sorted_events[0].dict() if sorted_events else None,
            'latest_event': sorted_events[-1].dict() if sorted_events else None,
            'total_timespan': (sorted_events[-1].timestamp - sorted_events[0].timestamp).total_seconds() if sorted_events else 0
        }

        return results

    def evaluate_causality_query(self, query: str, events: List[TemporalEvent]) -> Dict[str, Any]:
        """
        Evaluate queries about causality
        """
        analysis = self.causality_analyzer.analyze_causality(events)

        return {
            'query': query,
            'causality_analysis': analysis,
            'primary_causal_chains': self.identify_primary_causal_chains(analysis),
            'confidence_levels': analysis['causality_confidence_scores']
        }

    def identify_primary_causal_chains(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify the most significant causal chains from analysis
        """
        chains = []
        direct_causes = analysis.get('direct_causes', [])

        # Group direct causes by effect
        effects_map = {}
        for cause in direct_causes:
            effect_id = cause['effect_event_id']
            if effect_id not in effects_map:
                effects_map[effect_id] = []
            effects_map[effect_id].append(cause)

        # Identify chains with high confidence
        for effect_id, causes in effects_map.items():
            high_confidence_causes = [c for c in causes if c['confidence'] > 0.7]
            if high_confidence_causes:
                chains.append({
                    'effect_event': effect_id,
                    'primary_causes': high_confidence_causes,
                    'aggregate_confidence': sum(c['confidence'] for c in high_confidence_causes) / len(high_confidence_causes)
                })

        return chains

    def evaluate_counterfactual_query(self, query: str, events: List[TemporalEvent]) -> Dict[str, Any]:
        """
        Evaluate counterfactual reasoning queries
        """
        if not events:
            return {'query': query, 'error': 'No events to reason about'}

        # Take the most recent event for counterfactual analysis
        most_recent_event = max(events, key=lambda e: e.timestamp)

        # Extract potential alternative from query (simplified)
        alternatives = ['changed_approach', 'acted_earlier', 'consulted_expert']
        results = []

        for alt in alternatives:
            scenario = self.counterfactual_reasoner.generate_counterfactual_scenario(most_recent_event, alt)
            results.append({
                'alternative_action': alt,
                'scenario': scenario,
                'most_likely_outcome': max(scenario['probability_assessment'].items(), key=lambda x: x[1])[0] if scenario['probability_assessment'] else None
            })

        return {
            'query': query,
            'original_event': most_recent_event.dict(),
            'counterfactual_scenarios': results
        }

    def evaluate_predictive_query(self, query: str, events: List[TemporalEvent]) -> Dict[str, Any]:
        """
        Evaluate predictive reasoning queries
        """
        patterns = self.identify_temporal_patterns(events)
        predictors = self.extract_predictive_indicators(events)

        return {
            'query': query,
            'temporal_patterns': patterns,
            'predictive_indicators': predictors,
            'next_expected_events': self.predict_next_events(events, patterns, predictors),
            'confidence_intervals': [0.7, 0.85]  # Simplified confidence
        }

    def predict_next_events(self, events: List[TemporalEvent],
                          patterns: List[Dict[str, Any]],
                          predictors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Predict the next likely events based on patterns and predictors
        """
        predictions = []

        # Use periodic patterns to predict regular events
        for pattern in patterns:
            if pattern['type'] == 'periodic_pattern':
                if events:
                    last_event = max(events, key=lambda e: e.timestamp)
                    predicted_time = last_event.timestamp + timedelta(seconds=pattern['average_interval_seconds'])
                    predictions.append({
                        'predicted_event_type': f"recurring_{last_event.event_type}",
                        'estimated_time': predicted_time.isoformat(),
                        'confidence': pattern['regularity_score'],
                        'based_on_pattern': pattern['type']
                    })

        # Use predictive indicators
        for predictor in predictors:
            predictions.append({
                'predicted_event_type': f"follow_up_to_{predictor['predicted_event']}",
                'estimated_time': (datetime.now() + timedelta(seconds=predictor['typical_lead_time'])).isoformat(),
                'confidence': predictor['confidence'],
                'based_on_indicator': f"leading_event_{predictor['leading_event']}"
            })

        return predictions

    async def run_temporal_monitoring_loop(self):
        """
        Run a continuous monitoring loop for temporal reasoning
        """
        logger.info("Starting temporal reasoning monitoring loop...")

        while True:
            try:
                # Perform periodic temporal consistency checks
                active_events = [e for e in self.events.values()
                               if (datetime.now() - e.updated_at).total_seconds() < 3600]  # Last hour

                if active_events:
                    # Analyze recent events
                    recent_ids = [e.id for e in active_events]
                    analysis = self.analyze_temporal_sequence(recent_ids)

                    # Log significant findings
                    if analysis['paradox_check']:
                        logger.warning(f"Paradox detected in recent events: {analysis['paradox_check']}")

                    if analysis['anomaly_detection']:
                        logger.info(f"Temporal anomalies detected: {len(analysis['anomaly_detection'])}")

                # Sleep before next iteration
                await asyncio.sleep(10.0)  # Check every 10 seconds

            except Exception as e:
                logger.error(f"Error in temporal monitoring loop: {e}")
                await asyncio.sleep(30.0)  # Longer sleep on error


# Singleton instance
temporal_reasoning_engine = TemporalReasoningEngine()


def get_temporal_reasoning_engine():
    """
    Get the singleton temporal reasoning engine instance
    """
    return temporal_reasoning_engine


if __name__ == "__main__":
    # Example usage
    import asyncio

    # Get the engine
    engine = get_temporal_reasoning_engine()

    print("Creating temporal events...")

    # Create some events
    event1 = engine.create_temporal_event("email_sent", "Sent quarterly report to stakeholders",
                                         datetime.now() - timedelta(hours=2))
    event2 = engine.create_temporal_event("meeting_scheduled", "Scheduled follow-up meeting",
                                         datetime.now() - timedelta(hours=1))
    event3 = engine.create_temporal_event("analysis_completed", "Completed market analysis",
                                         datetime.now())

    print(f"Created events: {event1.event_type}, {event2.event_type}, {event3.event_type}")

    # Analyze the sequence
    print("\nAnalyzing temporal sequence...")
    analysis = engine.analyze_temporal_sequence([event1.id, event2.id, event3.id])
    print(f"Causality analysis: {len(analysis['causality_analysis']['direct_causes'])} direct causes found")
    print(f"Temporal patterns: {len(analysis['temporal_patterns'])} patterns found")
    print(f"Predictive indicators: {len(analysis['predictive_indicators'])} indicators found")

    # Perform counterfactual reasoning
    print("\nPerforming counterfactual reasoning...")
    counterfactual_result = engine.perform_counterfactual_reasoning(
        event1.id, "scheduled email for later time"
    )
    print(f"Counterfactual scenario generated for event {event1.id}")

    # Manipulate temporal flow (simulation)
    print("\nSimulating temporal flow manipulation...")
    manipulation_result = engine.manipulate_temporal_flow("accelerate", event2.id, timedelta(minutes=30))
    print(f"Temporal manipulation result: {manipulation_result['status']}")

    # Evaluate a temporal query
    print("\nEvaluating temporal query...")
    query_result = engine.evaluate_temporal_query(
        "What caused the analysis to be completed after the meeting was scheduled?",
        [event1.id, event2.id, event3.id]
    )
    print(f"Query evaluation found {len(query_result.get('causality_analysis', {}).get('direct_causes', []))} potential causes")

    # Run the monitoring loop
    print("\nStarting temporal monitoring loop (press Ctrl+C to stop)...")
    try:
        asyncio.run(engine.run_temporal_monitoring_loop())
    except KeyboardInterrupt:
        print("\nStopping temporal monitoring...")
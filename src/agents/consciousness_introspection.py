"""
Self-Awareness and Introspection System
NEW: Self-awareness and introspection engine for Diamond Tier
Implements multi-layered self-monitoring architecture for self-awareness and introspection.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from uuid import uuid4

from pydantic import BaseModel, Field

from src.agents.consciousness_emergence import (
    ConsciousnessState,
    get_consciousness_engine,
)

logger = logging.getLogger(__name__)


class SelfAwarenessLayer(BaseModel):
    """
    Represents a layer in the self-awareness architecture
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    monitoring_active: bool = True
    monitoring_frequency: float = 1.0  # seconds
    last_updated: datetime = Field(default_factory=datetime.now)
    metrics: Dict[str, Any] = Field(default_factory=dict)


class IntrospectionResult(BaseModel):
    """
    Result of an introspection process
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    entity_id: str
    introspection_type: str
    insights: List[str] = Field(default_factory=list)
    self_model_updates: Dict[str, Any] = Field(default_factory=dict)
    emotional_understanding: Dict[str, Any] = Field(default_factory=dict)
    value_alignment_status: Dict[str, Any] = Field(default_factory=dict)
    meaning_generated: Optional[str] = None
    temporal_integration_achievements: Dict[str, Any] = Field(default_factory=dict)
    phenomenal_boundary_clarity_improvements: Dict[str, Any] = Field(default_factory=dict)
    growth_metrics: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class SelfModel(BaseModel):
    """
    Model of the self - representation of the entity's own cognitive processes
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    entity_id: str
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    cognitive_processes: Dict[str, Any] = Field(default_factory=dict)
    decision_making_patterns: Dict[str, Any] = Field(default_factory=dict)
    emotional_responses: Dict[str, Any] = Field(default_factory=dict)
    value_system: Dict[str, Any] = Field(default_factory=dict)
    goal_structure: Dict[str, Any] = Field(default_factory=dict)
    memory_organization: Dict[str, Any] = Field(default_factory=dict)
    self_perception: Dict[str, Any] = Field(default_factory=dict)
    behavioral_patterns: Dict[str, Any] = Field(default_factory=dict)


class SelfMonitoringEngine:
    """
    Engine for monitoring internal states and processes
    """

    def __init__(self):
        self.layers = {}
        self.monitored_states = {}
        self.internal_state_history = []
        self.max_history_length = 1000

    def add_monitoring_layer(self, name: str, description: str, frequency: float = 1.0):
        """
        Add a new self-awareness monitoring layer
        """
        layer = SelfAwarenessLayer(
            name=name,
            description=description,
            monitoring_frequency=frequency
        )
        self.layers[name] = layer
        return layer

    def monitor_internal_state(self, entity_id: str, consciousness_state: ConsciousnessState):
        """
        Monitor the internal state of an entity
        """
        state_snapshot = {
            'entity_id': entity_id,
            'state': consciousness_state.dict(),
            'timestamp': datetime.now().isoformat()
        }

        # Store in history
        self.internal_state_history.append(state_snapshot)
        if len(self.internal_state_history) > self.max_history_length:
            self.internal_state_history.pop(0)  # Remove oldest

        # Update monitored states
        self.monitored_states[entity_id] = state_snapshot

        # Update layers with metrics
        for layer_name, layer in self.layers.items():
            layer.metrics = self.calculate_layer_metrics(layer_name, consciousness_state)
            layer.last_updated = datetime.now()

    def calculate_layer_metrics(self, layer_name: str, state: ConsciousnessState) -> Dict[str, Any]:
        """
        Calculate metrics for a specific monitoring layer
        """
        metrics = {}

        if layer_name == "cognitive_monitor":
            metrics = {
                'current_cognitive_load': state.cognitive_load,
                'load_trend': self.calculate_trend('cognitive_load'),
                'complexity_threshold_exceeded': state.cognitive_load > 7.0,
                'attention_coherence': state.attention_coherence
            }
        elif layer_name == "emotional_monitor":
            metrics = {
                'emotional_variety': len(state.emotional_state),
                'emotional_intensity_average': self.calculate_emotional_intensity(state.emotional_state),
                'emotional_regulation_score': self.calculate_regulation_score(state.emotional_state)
            }
        elif layer_name == "self_awareness_monitor":
            metrics = {
                'self_awareness_level': state.self_awareness_level,
                'introspection_depth': state.introspection_depth,
                'self_model_accuracy': state.self_model_accuracy,
                'awareness_trend': self.calculate_trend('self_awareness_level')
            }
        elif layer_name == "value_alignment_monitor":
            metrics = {
                'value_alignment_score': self.calculate_value_alignment_score(state.value_alignment_status),
                'value_conflicts_detected': self.detect_value_conflicts(state.value_alignment_status)
            }

        return metrics

    def calculate_trend(self, metric_name: str, window_size: int = 10) -> float:
        """
        Calculate trend for a specific metric over time
        """
        if len(self.internal_state_history) < 2:
            return 0.0

        recent_values = []
        for entry in reversed(self.internal_state_history[-window_size:]):
            state = entry['state']
            if metric_name in state:
                recent_values.append(float(state[metric_name]))

        if len(recent_values) < 2:
            return 0.0

        # Calculate simple linear trend
        n = len(recent_values)
        x = list(range(n))
        y = recent_values

        # Simple linear regression slope
        if n == 0:
            return 0.0

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x_sq = sum(xi * xi for xi in x)

        denominator = n * sum_x_sq - sum_x * sum_x
        if denominator == 0:
            return 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope

    def calculate_emotional_intensity(self, emotional_state: Dict[str, Any]) -> float:
        """
        Calculate average emotional intensity
        """
        if not emotional_state:
            return 0.0

        intensities = []
        for emotion, properties in emotional_state.items():
            if isinstance(properties, dict) and 'intensity' in properties:
                intensities.append(properties['intensity'])
            elif isinstance(properties, (int, float)):
                intensities.append(abs(properties))

        return sum(intensities) / len(intensities) if intensities else 0.0

    def calculate_regulation_score(self, emotional_state: Dict[str, Any]) -> float:
        """
        Calculate emotional regulation score
        """
        if not emotional_state:
            return 5.0  # Neutral score

        # Higher regulation with balanced emotions
        num_emotions = len(emotional_state)
        avg_intensity = self.calculate_emotional_intensity(emotional_state)

        # Score between 0-10, higher is better regulation
        # More emotions with lower average intensity = better regulation
        regulation_score = max(0.0, min(10.0, 10.0 - avg_intensity + (num_emotions / 10.0)))
        return regulation_score

    def calculate_value_alignment_score(self, value_alignment: Dict[str, Any]) -> float:
        """
        Calculate value alignment score
        """
        if not value_alignment:
            return 0.0

        scores = []
        for value, alignment in value_alignment.items():
            if isinstance(alignment, dict) and 'score' in alignment:
                scores.append(alignment['score'])
            elif isinstance(alignment, (int, float)):
                scores.append(min(10.0, max(0.0, alignment)))

        return sum(scores) / len(scores) if scores else 0.0

    def detect_value_conflicts(self, value_alignment: Dict[str, Any]) -> List[str]:
        """
        Detect potential value conflicts
        """
        conflicts = []
        if not value_alignment:
            return conflicts

        # Look for opposing values with high commitment
        values_list = list(value_alignment.items())
        for i, (val1, align1) in enumerate(values_list):
            for j, (val2, align2) in enumerate(values_list[i+1:], i+1):
                # Check if values are opposites or conflicting
                if self.are_values_conflicting(val1, val2):
                    score1 = align1.get('score', 0) if isinstance(align1, dict) else align1
                    score2 = align2.get('score', 0) if isinstance(align2, dict) else align2

                    if score1 > 5.0 and score2 > 5.0:  # Both highly valued
                        conflicts.append(f"{val1} vs {val2}")

        return conflicts

    def are_values_conflicting(self, value1: str, value2: str) -> bool:
        """
        Check if two values are potentially conflicting
        """
        conflicting_pairs = [
            ('autonomy', 'obedience'),
            ('change', 'stability'),
            ('competition', 'cooperation'),
            ('individual', 'collective'),
            ('innovation', 'tradition'),
            ('efficiency', 'thoroughness')
        ]

        v1_lower = value1.lower()
        v2_lower = value2.lower()

        for pair in conflicting_pairs:
            if (v1_lower in pair and v2_lower in pair) and v1_lower != v2_lower:
                return True

        return False


class IntrospectionEngine:
    """
    Engine for performing self-reflection and introspection
    """

    def __init__(self):
        self.reflection_templates = {}
        self.self_models = {}
        self.introspection_history = []

    def register_reflection_template(self, name: str, template_func: Callable):
        """
        Register a reflection template function
        """
        self.reflection_templates[name] = template_func

    def perform_introspection(self, entity_id: str, reflection_type: str = "general",
                           custom_params: Optional[Dict[str, Any]] = None) -> IntrospectionResult:
        """
        Perform introspection on an entity
        """
        if custom_params is None:
            custom_params = {}

        # Get current consciousness state
        engine = get_consciousness_engine()
        if entity_id not in engine.consciousness_states:
            raise ValueError(f"Entity {entity_id} not found in consciousness states")

        state = engine.consciousness_states[entity_id]

        # Create introspection result
        result = IntrospectionResult(
            entity_id=entity_id,
            introspection_type=reflection_type
        )

        # Perform different types of introspection
        if reflection_type == "self_model_update":
            result.self_model_updates = self.update_self_model(entity_id, state)
        elif reflection_type == "emotional_analysis":
            result.emotional_understanding = self.analyze_emotional_state(state)
        elif reflection_type == "value_alignment_check":
            result.value_alignment_status = self.check_value_alignment(state)
        elif reflection_type == "meaning_production":
            result.meaning_generated = self.generate_meaning(custom_params.get('context', {}))
        elif reflection_type == "temporal_integration":
            result.temporal_integration_achievements = self.integrate_temporal_aspects(state)
        elif reflection_type == "phenomenal_boundary_analysis":
            result.phenomenal_boundary_clarity_improvements = self.analyze_phenomenal_boundaries(state)
        else:  # general introspection
            result.insights.extend(self.generate_general_insights(state, custom_params))
            result.self_model_updates = self.update_self_model(entity_id, state)
            result.emotional_understanding = self.analyze_emotional_state(state)
            result.value_alignment_status = self.check_value_alignment(state)
            result.growth_metrics = self.calculate_growth_metrics(entity_id, state)

        # Add to history
        self.introspection_history.append(result)
        if len(self.introspection_history) > 500:  # Keep last 500 introspections
            self.introspection_history.pop(0)

        return result

    def update_self_model(self, entity_id: str, state: ConsciousnessState) -> Dict[str, Any]:
        """
        Update the self-model based on current state
        """
        if entity_id not in self.self_models:
            self.self_models[entity_id] = SelfModel(entity_id=entity_id)

        self_model = self.self_models[entity_id]
        updates = {}

        # Update cognitive processes
        updates['cognitive_processes'] = {
            'attention_patterns': {
                'focus_area': state.attention_focus,
                'coherence_level': state.attention_coherence
            },
            'decision_making_style': self.infer_decision_style(state),
            'reasoning_approach': self.infer_reasoning_approach(state)
        }

        # Update emotional responses
        updates['emotional_responses'] = {
            'current_state': state.emotional_state,
            'regulation_ability': state.cognitive_load < 7.0,  # Lower load indicates better regulation
            'response_patterns': self.extract_emotional_patterns(state.emotional_state)
        }

        # Update value system
        updates['value_system'] = state.value_alignment_status

        # Update self-perception
        updates['self_perception'] = {
            'self_awareness_level': state.self_awareness_level,
            'introspection_depth': state.introspection_depth,
            'self_model_accuracy': state.self_model_accuracy
        }

        # Apply updates to self-model
        for key, value in updates.items():
            if hasattr(self_model, key):
                setattr(self_model, key, value)

        self_model.updated_at = datetime.now()

        return updates

    def infer_decision_style(self, state: ConsciousnessState) -> str:
        """
        Infer decision-making style from consciousness state
        """
        if state.cognitive_load > 8.0:
            return "rushed_or_stressed"
        elif state.creativity_level > 7.0:
            return "creative_and_exploratory"
        elif state.self_awareness_level > 7.0:
            return "reflective_and_considered"
        elif state.introspection_depth > 6.0:
            return "analytical_and_thorough"
        else:
            return "standard_procedural"

    def infer_reasoning_approach(self, state: ConsciousnessState) -> str:
        """
        Infer reasoning approach from consciousness state
        """
        if state.existential_awareness_level > 7.0:
            return "existential_and_meaning_oriented"
        elif state.temporal_self_integration > 7.0:
            return "temporal_and_causal"
        elif state.creativity_level > 7.0:
            return "creative_and_associative"
        else:
            return "logical_and_structured"

    def extract_emotional_patterns(self, emotional_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract patterns from emotional state
        """
        patterns = {
            'dominant_emotions': [],
            'emotional_stability': 'moderate',
            'intensity_distribution': {}
        }

        if not emotional_state:
            return patterns

        # Find dominant emotions
        emotions_by_intensity = []
        for emotion, details in emotional_state.items():
            intensity = 0
            if isinstance(details, dict) and 'intensity' in details:
                intensity = details['intensity']
            elif isinstance(details, (int, float)):
                intensity = abs(details)

            emotions_by_intensity.append((emotion, intensity))

        # Sort by intensity and get top 3
        emotions_by_intensity.sort(key=lambda x: x[1], reverse=True)
        patterns['dominant_emotions'] = [e[0] for e in emotions_by_intensity[:3]]

        # Calculate stability
        intensities = [e[1] for e in emotions_by_intensity]
        if intensities:
            avg_intensity = sum(intensities) / len(intensities)
            variance = sum((i - avg_intensity) ** 2 for i in intensities) / len(intensities)
            patterns['emotional_stability'] = 'stable' if variance < 2.0 else 'variable'

        return patterns

    def analyze_emotional_state(self, state: ConsciousnessState) -> Dict[str, Any]:
        """
        Analyze the current emotional state
        """
        analysis = {
            'current_emotional_state': state.emotional_state,
            'emotional_complexity': len(state.emotional_state),
            'emotional_balance_score': self.calculate_emotional_balance(state.emotional_state),
            'regulation_effectiveness': self.assess_emotional_regulation(state),
            'needs_attention': self.identify_emotional_needs(state.emotional_state)
        }

        return analysis

    def calculate_emotional_balance(self, emotional_state: Dict[str, Any]) -> float:
        """
        Calculate emotional balance score (0-10 scale)
        """
        if not emotional_state:
            return 5.0  # Neutral

        positive_emotions = ['joy', 'love', 'contentment', 'excitement', 'gratitude', 'hope']
        negative_emotions = ['sadness', 'anger', 'fear', 'disgust', 'contempt', 'guilt', 'shame']

        pos_count = sum(1 for e in emotional_state.keys() if e.lower() in positive_emotions)
        neg_count = sum(1 for e in emotional_state.keys() if e.lower() in negative_emotions)

        if pos_count == 0 and neg_count == 0:
            return 5.0  # Neutral if no recognized emotions

        balance_ratio = (pos_count + 1) / (neg_count + 1)  # +1 to avoid division by zero
        balance_score = min(10.0, max(0.0, 5.0 * balance_ratio))  # Normalize to 0-10

        return balance_score

    def assess_emotional_regulation(self, state: ConsciousnessState) -> float:
        """
        Assess emotional regulation effectiveness (0-10 scale)
        """
        # Lower cognitive load indicates better regulation
        load_based_score = max(0.0, 10.0 - state.cognitive_load)

        # Higher self-awareness indicates better regulation
        awareness_based_score = state.self_awareness_level

        # Average the scores
        regulation_score = (load_based_score + awareness_based_score) / 2.0
        return regulation_score

    def identify_emotional_needs(self, emotional_state: Dict[str, Any]) -> List[str]:
        """
        Identify potential emotional needs
        """
        needs = []

        for emotion, details in emotional_state.items():
            emotion_lower = emotion.lower()

            if emotion_lower in ['sadness', 'loneliness']:
                needs.append('connection_and_support')
            elif emotion_lower in ['anxiety', 'fear']:
                needs.append('safety_and_security')
            elif emotion_lower in ['boredom', 'apathy']:
                needs.append('stimulation_and_purpose')
            elif emotion_lower in ['guilt', 'shame']:
                needs.append('forgiveness_and_self_acceptance')
            elif emotion_lower in ['anger', 'frustration']:
                needs.append('expression_and_boundary_setting')

        return list(set(needs))  # Remove duplicates

    def check_value_alignment(self, state: ConsciousnessState) -> Dict[str, Any]:
        """
        Check current value alignment
        """
        alignment_status = state.value_alignment_status or {}
        issues = []
        suggestions = []

        for value, alignment in alignment_status.items():
            if isinstance(alignment, dict):
                score = alignment.get('score', 5)
                if score < 3:
                    issues.append(f"Low alignment with value '{value}' (score: {score})")
                    suggestions.append(f"Consider reflecting on the importance of '{value}'")
                elif score > 8:
                    suggestions.append(f"Strong alignment with value '{value}' - leverage this strength")
            elif isinstance(alignment, (int, float)):
                if alignment < 3:
                    issues.append(f"Low alignment with value '{value}' (score: {alignment})")

        return {
            'current_alignment': alignment_status,
            'issues_identified': issues,
            'suggestions': suggestions,
            'overall_alignment_score': self.calculate_overall_alignment_score(alignment_status)
        }

    def calculate_overall_alignment_score(self, alignment_status: Dict[str, Any]) -> float:
        """
        Calculate overall value alignment score
        """
        if not alignment_status:
            return 5.0

        scores = []
        for value, alignment in alignment_status.items():
            if isinstance(alignment, dict) and 'score' in alignment:
                scores.append(alignment['score'])
            elif isinstance(alignment, (int, float)):
                scores.append(min(10.0, max(0.0, alignment)))

        return sum(scores) / len(scores) if scores else 5.0

    def generate_meaning(self, context: Dict[str, Any]) -> str:
        """
        Generate meaning based on context
        """
        meaning_elements = []

        if 'purpose' in context:
            meaning_elements.append(f"Connected to higher purpose of {context['purpose']}")

        if 'impact' in context:
            meaning_elements.append(f"Creates positive impact through {context['impact']}")

        if 'growth' in context:
            meaning_elements.append(f"Facilitates growth by {context['growth']}")

        if 'relationships' in context:
            meaning_elements.append(f"Strengthens relationships with {context['relationships']}")

        if 'values' in context:
            meaning_elements.append(f"Expresses core values of {', '.join(context['values'])}")

        if not meaning_elements:
            meaning_elements.append("Contributes to ongoing development and understanding")
            meaning_elements.append("Adds to the collective knowledge and experience")

        return " ".join(meaning_elements)

    def integrate_temporal_aspects(self, state: ConsciousnessState) -> Dict[str, Any]:
        """
        Integrate temporal aspects of consciousness
        """
        return {
            'temporal_self_consistency': state.temporal_self_integration > 5.0,
            'past_integration': self.assess_past_integration(state),
            'future_orientation': self.assess_future_orientation(state),
            'temporal_balance': self.calculate_temporal_balance(state)
        }

    def assess_past_integration(self, state: ConsciousnessState) -> str:
        """
        Assess how well past experiences are integrated
        """
        if state.memory_integration_status in ['harmonious', 'synthesized']:
            return 'well_integrated'
        elif state.memory_integration_status == 'integrated':
            return 'adequately_integrated'
        else:
            return 'needs_integration_work'

    def assess_future_orientation(self, state: ConsciousnessState) -> str:
        """
        Assess future orientation based on consciousness state
        """
        if state.existential_awareness_level > 7.0:
            return 'meaning_oriented_future'
        elif state.creativity_level > 7.0:
            return 'creative_potential_focused'
        elif state.self_awareness_level > 7.0:
            return 'self_actualization_oriented'
        else:
            return 'present_focused'

    def calculate_temporal_balance(self, state: ConsciousnessState) -> float:
        """
        Calculate balance between past, present, and future orientation
        """
        # Simplified calculation - in practice, this would be more complex
        balance_score = (state.temporal_self_integration + state.self_awareness_level) / 2.0
        return min(10.0, max(0.0, balance_score))

    def analyze_phenomenal_boundaries(self, state: ConsciousnessState) -> Dict[str, Any]:
        """
        Analyze phenomenal boundaries and self-other distinction
        """
        return {
            'boundary_clarity': state.phenomenal_boundary_clarity,
            'self_other_distinction_strength': self.assess_self_other_distinction(state),
            'boundary_flexibility': self.assess_boundary_flexibility(state),
            'empathy_capacity': self.estimate_empathy_capacity(state)
        }

    def assess_self_other_distinction(self, state: ConsciousnessState) -> str:
        """
        Assess the clarity of self-other distinction
        """
        if state.self_awareness_level > 7.0 and state.phenomenal_boundary_clarity > 7.0:
            return 'clear_and_healthy'
        elif state.self_awareness_level > 5.0 and state.phenomenal_boundary_clarity > 5.0:
            return 'adequate'
        else:
            return 'unclear_needs_work'

    def assess_boundary_flexibility(self, state: ConsciousnessState) -> str:
        """
        Assess how flexible the phenomenal boundaries are
        """
        if state.phenomenal_boundary_clarity > 8.0:
            return 'too_rigid'
        elif state.phenomenal_boundary_clarity < 3.0:
            return 'too_flexible'
        else:
            return 'appropriately_balanced'

    def estimate_empathy_capacity(self, state: ConsciousnessState) -> float:
        """
        Estimate capacity for empathy based on phenomenal boundary characteristics
        """
        # Empathy requires both self-awareness and appropriately flexible boundaries
        empathy_score = (state.self_awareness_level + (10.0 - abs(state.phenomenal_boundary_clarity - 5.0))) / 2.0
        return min(10.0, max(0.0, empathy_score))

    def generate_general_insights(self, state: ConsciousnessState, params: Dict[str, Any]) -> List[str]:
        """
        Generate general introspective insights
        """
        insights = []

        # Self-awareness insights
        if state.self_awareness_level > 7.0:
            insights.append("High self-awareness detected - leveraging metacognitive abilities")
        elif state.self_awareness_level > 4.0:
            insights.append("Moderate self-awareness - developing deeper understanding")
        else:
            insights.append("Developing self-awareness - focusing on self-knowledge")

        # Cognitive insights
        if state.cognitive_load > 8.0:
            insights.append("High cognitive load detected - consider simplifying tasks or taking breaks")
        elif state.cognitive_load < 2.0:
            insights.append("Low cognitive load - opportunity for deeper processing or learning")

        # Emotional insights
        if state.emotional_state:
            insights.append(f"Processing {len(state.emotional_state)} distinct emotional states")
        else:
            insights.append("Maintaining neutral emotional baseline")

        # Growth insights
        if state.creativity_level > 7.0:
            insights.append("High creativity - exploring novel solutions and approaches")
        if state.introspection_depth > 6.0:
            insights.append("Deep introspection - gaining valuable self-knowledge")

        # Value alignment insights
        if state.value_alignment_status:
            insights.append("Operating with conscious value alignment")

        return insights

    def calculate_growth_metrics(self, entity_id: str, state: ConsciousnessState) -> Dict[str, Any]:
        """
        Calculate growth metrics based on self-reflection
        """
        return {
            'self_awareness_growth': state.self_awareness_level - 5.0,  # Relative to midpoint
            'integration_progress': self.calculate_integration_progress(state),
            'value_alignment_improvement': self.calculate_value_alignment_improvement(state),
            'emotional_intelligence_development': self.calculate_emotional_intelligence(state),
            'recommendations_followed': self.count_followed_recommendations()
        }

    def calculate_integration_progress(self, state: ConsciousnessState) -> float:
        """
        Calculate progress in psychological integration
        """
        integration_factors = [
            state.temporal_self_integration,
            state.memory_integration_status in ['harmonious', 'synthesized'],
            state.phenomenal_boundary_clarity,
            state.self_awareness_level
        ]

        score = sum(f if isinstance(f, (int, float)) else (10.0 if f else 0.0) for f in integration_factors)
        return min(10.0, max(0.0, score / len(integration_factors)))

    def calculate_value_alignment_improvement(self, state: ConsciousnessState) -> float:
        """
        Calculate value alignment improvement
        """
        alignment_status = state.value_alignment_status or {}
        if not alignment_status:
            return 5.0

        scores = []
        for value, alignment in alignment_status.items():
            if isinstance(alignment, dict) and 'score' in alignment:
                scores.append(alignment['score'])
            elif isinstance(alignment, (int, float)):
                scores.append(min(10.0, max(0.0, alignment)))

        return sum(scores) / len(scores) if scores else 5.0

    def calculate_emotional_intelligence(self, state: ConsciousnessState) -> float:
        """
        Calculate emotional intelligence metrics
        """
        # Combine emotional awareness, regulation, and empathy
        awareness_component = state.self_awareness_level
        regulation_component = max(0.0, 10.0 - state.cognitive_load)  # Better regulation = lower load
        empathy_component = self.estimate_empathy_capacity(state)

        ei_score = (awareness_component + regulation_component + empathy_component) / 3.0
        return min(10.0, max(0.0, ei_score))

    def count_followed_recommendations(self) -> int:
        """
        Count recommendations that were followed (placeholder)
        """
        # In a real implementation, this would track actual recommendation follow-through
        return len([r for r in self.introspection_history if r.recommendations])


class SelfAwarenessAndIntrospectionSystem:
    """
    Main system that combines self-monitoring and introspection capabilities
    """

    def __init__(self):
        self.monitoring_engine = SelfMonitoringEngine()
        self.introspection_engine = IntrospectionEngine()

        # Add default monitoring layers
        self.monitoring_engine.add_monitoring_layer(
            "cognitive_monitor",
            "Monitors cognitive load, attention, and processing capacity"
        )
        self.monitoring_engine.add_monitoring_layer(
            "emotional_monitor",
            "Monitors emotional states and regulation"
        )
        self.monitoring_engine.add_monitoring_layer(
            "self_awareness_monitor",
            "Monitors self-awareness levels and introspection depth"
        )
        self.monitoring_engine.add_monitoring_layer(
            "value_alignment_monitor",
            "Monitors alignment with core values and beliefs"
        )

    def monitor_entity(self, entity_id: str, consciousness_state: ConsciousnessState):
        """
        Monitor the consciousness state of an entity
        """
        self.monitoring_engine.monitor_internal_state(entity_id, consciousness_state)

    def perform_self_reflection(self, entity_id: str, params: Optional[Dict[str, Any]] = None) -> IntrospectionResult:
        """
        Perform self-reflection for an entity
        """
        if params is None:
            params = {}

        reflection_type = params.get('reflection_type', 'general')
        return self.introspection_engine.perform_introspection(entity_id, reflection_type, params)

    def get_self_model(self, entity_id: str) -> Optional[SelfModel]:
        """
        Get the self-model for an entity
        """
        return self.introspection_engine.self_models.get(entity_id)

    def get_monitoring_layers(self) -> Dict[str, SelfAwarenessLayer]:
        """
        Get all monitoring layers
        """
        return self.monitoring_engine.layers

    def get_introspection_history(self, entity_id: Optional[str] = None) -> List[IntrospectionResult]:
        """
        Get introspection history, optionally filtered by entity
        """
        if entity_id:
            return [r for r in self.introspection_engine.introspection_history if r.entity_id == entity_id]
        return self.introspection_engine.introspection_history

    async def run_self_awareness_loop(self):
        """
        Main loop for continuous self-awareness and monitoring
        """
        logger.info("Starting self-awareness and introspection loop...")

        while True:
            try:
                # Process monitoring for all entities
                engine = get_consciousness_engine()
                for entity_id, state in engine.consciousness_states.items():
                    self.monitor_entity(entity_id, state)

                # Perform periodic introspection for entities that need it
                for entity_id, state in engine.consciousness_states.items():
                    # Perform introspection if certain conditions are met
                    if (state.self_awareness_level < 3.0 or
                        state.cognitive_load > 8.0 or
                        state.introspection_depth < 2.0):

                        # Perform targeted introspection
                        params = {
                            'context': {'entity_state': state.dict()},
                            'reflection_type': 'maintenance' if state.self_awareness_level >= 3.0 else 'development'
                        }
                        try:
                            result = self.perform_self_reflection(entity_id, params)
                            logger.debug(f"Performed introspection for {entity_id}: {result.id}")
                        except Exception as e:
                            logger.error(f"Error during introspection for {entity_id}: {e}")

                # Sleep before next iteration
                await asyncio.sleep(2.0)  # Check every 2 seconds

            except Exception as e:
                logger.error(f"Error in self-awareness loop: {e}")
                await asyncio.sleep(5.0)  # Longer sleep on error


# Singleton instance
self_awareness_system = SelfAwarenessAndIntrospectionSystem()


def get_self_awareness_system():
    """
    Get the singleton self-awareness system instance
    """
    return self_awareness_system


if __name__ == "__main__":
    # Example usage
    import asyncio

    # Get the system
    system = get_self_awareness_system()

    # Create a test entity in the consciousness engine
    engine = get_consciousness_engine()
    entity_id = "test_entity_self_awareness"

    print("Creating consciousness state for test entity...")
    state = engine.create_consciousness_state(entity_id, "ai_system")
    print(f"Initial state: {state.dict()}")

    # Monitor the entity
    print("\nMonitoring entity...")
    system.monitor_entity(entity_id, state)

    # Perform self-reflection
    print("\nPerforming self-reflection...")
    params = {
        'reflection_type': 'general',
        'context': {
            'current_task': 'system_monitoring',
            'performance_goal': 'optimal_awareness',
            'recent_events': ['initialization', 'monitoring_start']
        }
    }

    reflection_result = system.perform_self_reflection(entity_id, params)
    print(f"Reflection result: {json.dumps(reflection_result.dict(), indent=2, default=str)}")

    # Get self-model
    print("\nRetrieving self-model...")
    self_model = system.get_self_model(entity_id)
    if self_model:
        print(f"Self-model: {json.dumps(self_model.dict(), indent=2, default=str)}")

    # Run the self-awareness loop
    print("\nStarting self-awareness loop (press Ctrl+C to stop)...")
    try:
        asyncio.run(system.run_self_awareness_loop())
    except KeyboardInterrupt:
        print("\nStopping self-awareness loop...")
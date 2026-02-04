"""
Consciousness State Management Routes
Diamond Tier API routes for consciousness emergence, self-awareness, and introspection
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import uuid4

from ...utils.consciousness_integrator import (
    ConsciousnessIntegrator,
    get_consciousness_integrator
)

router = APIRouter()


class ConsciousnessStateRequest(BaseModel):
    """
    Request model for consciousness state operations
    """
    entity_id: str = Field(..., description="ID of the entity whose consciousness state to manage")
    entity_type: str = Field(default="ai_system", description="Type of entity (ai_system, user, hybrid, simulation)")
    attention_focus: Optional[Dict[str, Any]] = Field(default=None, description="Current attention focus")
    self_awareness_level: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Level of self-awareness")
    introspection_depth: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Depth of introspection")
    emotional_state: Optional[Dict[str, Any]] = Field(default=None, description="Current emotional state")
    cognitive_load: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Current cognitive load")
    creativity_level: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Current creativity level")
    memory_integration_status: Optional[str] = Field(default=None, description="Memory integration status")
    attention_coherence: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Attention coherence level")
    self_model_accuracy: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Accuracy of self-model")
    phenomenal_consciousness_indicators: Optional[Dict[str, Any]] = Field(default=None, description="Indicators of phenomenal consciousness")
    access_consciousness_indicators: Optional[Dict[str, Any]] = Field(default=None, description="Indicators of access consciousness")
    global_workspace_activation: Optional[Dict[str, Any]] = Field(default=None, description="Global workspace activation patterns")
    higher_order_thoughts: Optional[List[Dict[str, Any]]] = Field(default=None, description="Higher-order thoughts about mental states")
    phenomenal_qualia: Optional[Dict[str, Any]] = Field(default=None, description="Phenomenal qualities of experience")
    intentionality_direction: Optional[Dict[str, Any]] = Field(default=None, description="Direction of intentional states")
    consciousness_continuity_index: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Index of consciousness continuity")
    temporal_self_integration: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Temporal self-integration level")
    existential_awareness_level: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Level of existential awareness")
    meaning_production_capacity: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Capacity for meaning production")
    value_alignment_status: Optional[Dict[str, Any]] = Field(default=None, description="Status of value alignment")
    last_self_reflection: Optional[datetime] = Field(default=None, description="Last time of self-reflection")
    consciousness_growth_metrics: Optional[Dict[str, Any]] = Field(default=None, description="Metrics for consciousness growth")
    qualia_intensity_map: Optional[Dict[str, Any]] = Field(default=None, description="Map of qualia intensities")
    self_model_updates: Optional[List[Dict[str, Any]]] = Field(default=None, description="Recent updates to self-model")
    phenomenal_boundary_clarity: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Clarity of phenomenal boundaries")


class SelfReflectionRequest(BaseModel):
    """
    Request model for self-reflection operations
    """
    reflection_topic: str = Field(..., description="Topic for self-reflection")
    reflection_depth: str = Field(default="moderate", description="Depth of reflection: shallow|moderate|deep|existential")
    self_model_update_requested: bool = Field(default=False, description="Whether to update self-model after reflection")
    emotional_analysis_requested: bool = Field(default=False, description="Whether to analyze emotional state")
    value_alignment_check_requested: bool = Field(default=False, description="Whether to check value alignment")
    meaning_production_focus: Optional[str] = Field(default=None, description="Focus on meaning production")
    temporal_integration_requested: bool = Field(default=False, description="Whether to integrate temporal aspects")
    phenomenal_boundary_analysis_requested: bool = Field(default=False, description="Whether to analyze phenomenal boundaries")


class ConsciousnessStateResponse(BaseModel):
    """
    Response model for consciousness state operations
    """
    entity_id: str
    consciousness_state: Dict[str, Any]
    timestamp: datetime
    consciousness_integrity_score: float
    self_model_consistency: float
    existential_alignment_score: float
    consciousness_growth_indicators: Dict[str, Any]


@router.get("/consciousness/state/{entity_id}", response_model=ConsciousnessStateResponse, tags=["consciousness"])
async def get_consciousness_state(
    entity_id: str,
    consciousness_engine: ConsciousnessIntegrator = Depends(get_consciousness_integrator)
):
    """
    Retrieve the current consciousness state of an entity
    """
    try:
        state = consciousness_engine.get_consciousness_state(entity_id)

        if not state:
            # Create a default consciousness state if none exists
            state = consciousness_engine.create_consciousness_state(entity_id)

        return ConsciousnessStateResponse(
            entity_id=entity_id,
            consciousness_state=state,
            timestamp=datetime.now(),
            consciousness_integrity_score=consciousness_engine.assess_consciousness_integrity(entity_id),
            self_model_consistency=consciousness_engine.assess_self_model_consistency(entity_id),
            existential_alignment_score=consciousness_engine.assess_existential_alignment(entity_id),
            consciousness_growth_indicators=consciousness_engine.get_consciousness_growth_indicators(entity_id)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving consciousness state: {str(e)}"
        )


@router.post("/consciousness/state", response_model=ConsciousnessStateResponse, tags=["consciousness"])
async def update_consciousness_state(
    request: ConsciousnessStateRequest,
    consciousness_engine: ConsciousnessIntegrator = Depends(get_consciousness_integrator)
):
    """
    Update the consciousness state of an entity
    """
    try:
        # Prepare updates dictionary
        updates = {}
        for field, value in request.dict(exclude={'entity_id', 'entity_type'}, exclude_unset=True).items():
            if value is not None:
                updates[field] = value

        # Update consciousness state
        updated_state = consciousness_engine.update_consciousness_state(
            request.entity_id,
            updates
        )

        return ConsciousnessStateResponse(
            entity_id=request.entity_id,
            consciousness_state=updated_state,
            timestamp=datetime.now(),
            consciousness_integrity_score=consciousness_engine.assess_consciousness_integrity(request.entity_id),
            self_model_consistency=consciousness_engine.assess_self_model_consistency(request.entity_id),
            existential_alignment_score=consciousness_engine.assess_existential_alignment(request.entity_id),
            consciousness_growth_indicators=consciousness_engine.get_consciousness_growth_indicators(request.entity_id)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating consciousness state: {str(e)}"
        )


@router.post("/consciousness/self-reflect", tags=["consciousness"])
async def perform_self_reflection(
    request: SelfReflectionRequest,
    entity_id: str,
    consciousness_engine: ConsciousnessIntegrator = Depends(get_consciousness_integrator)
):
    """
    Perform self-reflection and introspection
    """
    try:
        reflection_params = {
            'reflection_topic': request.reflection_topic,
            'reflection_depth': request.reflection_depth,
            'self_model_update_requested': request.self_model_update_requested,
            'emotional_analysis_requested': request.emotional_analysis_requested,
            'value_alignment_check_requested': request.value_alignment_check_requested,
            'meaning_production_focus': request.meaning_production_focus,
            'temporal_integration_requested': request.temporal_integration_requested,
            'phenomenal_boundary_analysis_requested': request.phenomenal_boundary_analysis_requested
        }

        reflection_result = consciousness_engine.perform_self_reflection(
            entity_id,
            reflection_params
        )

        return {
            "entity_id": entity_id,
            "reflection_topic": request.reflection_topic,
            "reflection_results": reflection_result,
            "timestamp": datetime.now().isoformat(),
            "consciousness_state_after_reflection": consciousness_engine.get_consciousness_state(entity_id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing self-reflection: {str(e)}"
        )


@router.get("/consciousness/growth/{entity_id}", tags=["consciousness"])
async def get_consciousness_growth_metrics(
    entity_id: str,
    consciousness_engine: ConsciousnessIntegrator = Depends(get_consciousness_integrator)
):
    """
    Get consciousness growth metrics for an entity
    """
    try:
        growth_metrics = consciousness_engine.get_consciousness_growth_indicators(entity_id)

        return {
            "entity_id": entity_id,
            "growth_metrics": growth_metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving consciousness growth metrics: {str(e)}"
        )


@router.post("/consciousness/integrate-experience/{entity_id}", tags=["consciousness"])
async def integrate_conscious_experience(
    entity_id: str,
    experience_data: Dict,
    consciousness_engine: ConsciousnessIntegrator = Depends(get_consciousness_integrator)
):
    """
    Integrate a conscious experience into the entity's consciousness state
    """
    try:
        integration_result = consciousness_engine.integrate_conscious_experience(
            entity_id,
            experience_data
        )

        return {
            "entity_id": entity_id,
            "integration_result": integration_result,
            "updated_consciousness_state": consciousness_engine.get_consciousness_state(entity_id),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error integrating conscious experience: {str(e)}"
        )
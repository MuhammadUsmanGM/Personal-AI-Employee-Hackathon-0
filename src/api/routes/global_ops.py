"""
Global Operations API Routes for Platinum Tier
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ...services.database import get_db, GlobalOperation as GlobalOperationModel
from ..platinum_tier_models import (
    GlobalOperationRequest, GlobalOperationUpdate, GlobalOperationResponse,
    PaginatedGlobalOperations, GlobalOperationStatus, GlobalOperationPriority
)

router = APIRouter(prefix="/global", tags=["global-operations"])


@router.get("/operations", response_model=PaginatedGlobalOperations)
async def get_global_operations(
    db: Session = Depends(get_db),
    status: Optional[GlobalOperationStatus] = Query(None, description="Filter by status"),
    priority: Optional[GlobalOperationPriority] = Query(None, description="Filter by priority"),
    region: Optional[str] = Query(None, description="Filter by region"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
):
    """
    Retrieve list of global operations
    """
    try:
        # Build query filters
        query = db.query(GlobalOperationModel)

        if status:
            query = query.filter(GlobalOperationModel.status == status.value)
        if priority:
            query = query.filter(GlobalOperationModel.priority == priority.value)
        if region:
            # Assuming region is stored in regions_affected as JSON
            query = query.filter(GlobalOperationModel.regions_affected.contains([region]))

        # Calculate pagination
        total = query.count()
        operations = query.offset((page - 1) * size).limit(size).all()

        return PaginatedGlobalOperations(
            operations=[GlobalOperationResponse.from_orm(op) for op in operations],
            pagination={
                "page": page,
                "size": size,
                "total": total,
                "pages": (total + size - 1) // size
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving global operations: {str(e)}")


@router.post("/operations", response_model=GlobalOperationResponse, status_code=status.HTTP_201_CREATED)
async def create_global_operation(
    operation: GlobalOperationRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new global operation
    """
    try:
        # Create new global operation
        db_operation = GlobalOperationModel(
            operation_name=operation.operation_name,
            description=operation.description,
            organization_id=operation.organization_id,
            owner_id=operation.owner_id,
            status="planned",  # Default status
            priority=operation.priority.value if operation.priority else "medium",
            start_date=operation.start_date,
            end_date=operation.end_date,
            estimated_completion=operation.estimated_completion,
            regions_affected=operation.regions_affected,
            risk_assessment=operation.risk_assessment,
            resource_allocation=operation.resource_allocation,
            dependencies=operation.dependencies,
            success_metrics=operation.success_metrics,
            compliance_requirements=operation.compliance_requirements,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(db_operation)
        db.commit()
        db.refresh(db_operation)

        return GlobalOperationResponse.from_orm(db_operation)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating global operation: {str(e)}")


@router.put("/operations/{operation_id}", response_model=GlobalOperationResponse)
async def update_global_operation(
    operation_id: str,
    operation: GlobalOperationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a global operation
    """
    try:
        db_operation = db.query(GlobalOperationModel).filter(
            GlobalOperationModel.id == operation_id
        ).first()

        if not db_operation:
            raise HTTPException(status_code=404, detail="Global operation not found")

        # Update fields
        update_data = operation.dict(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_operation, field, value)

        db_operation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_operation)

        return GlobalOperationResponse.from_orm(db_operation)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating global operation: {str(e)}")


@router.delete("/operations/{operation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_global_operation(
    operation_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a global operation
    """
    try:
        db_operation = db.query(GlobalOperationModel).filter(
            GlobalOperationModel.id == operation_id
        ).first()

        if not db_operation:
            raise HTTPException(status_code=404, detail="Global operation not found")

        db.delete(db_operation)
        db.commit()

        return
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting global operation: {str(e)}")


@router.post("/tasks/distribute")
async def distribute_task_globally(
    task_data: dict,
    db: Session = Depends(get_db)
):
    """
    Distribute a task to multiple regions
    """
    try:
        # This would integrate with the orchestrator to distribute tasks globally
        # For now, we'll return a success response
        return {
            "message": "Task distribution initiated",
            "task_id": task_data.get("task_id"),
            "regions": task_data.get("regions", []),
            "status": "distributed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error distributing task: {str(e)}")


@router.get("/regions")
async def get_available_regions():
    """
    Get list of available regions
    """
    # In a real implementation, this would come from configuration
    return {
        "regions": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "sa-east-1"],
        "default_region": "us-east-1"
    }
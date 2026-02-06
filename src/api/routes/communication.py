"""
Communication API routes for AI Employee response system
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, Any
from datetime import datetime
import asyncio

from src.services.response_coordinator import ResponseCoordinator
from src.response_handlers.base_handler import CommunicationChannel, ResponseStatus
from src.services.conversation_tracker import ConversationTracker, ResponseType, Priority
from src.api.models.response_models import (
    SendResponseRequest,
    SendResponseResponse,
    ResponseStatusResponse,
    ConversationContextResponse,
    CommunicationChannel,
    ResponseType,
    Priority,
    ResponseStatus
)

# Create router for communication endpoints
communication_router = APIRouter(prefix="/communication", tags=["communication"])

def get_response_coordinator():
    """Dependency to get response coordinator instance"""
    # In a real implementation, this would be injected properly
    # For now, we'll create a basic instance
    from src.config.manager import get_config
    config = get_config()
    vault_path = config.get("vault_path", "./obsidian_vault")
    return ResponseCoordinator(vault_path=vault_path)

@communication_router.post("/send-response", response_model=SendResponseResponse)
async def send_response(
    request: SendResponseRequest,
    coordinator: ResponseCoordinator = Depends(get_response_coordinator)
):
    """
    Send a response back to a user through the specified communication channel
    """
    try:
        # Queue the response to be sent
        result = await coordinator.queue_response(
            original_message_id=request.original_message_id,
            channel=request.channel,
            recipient_identifier=request.recipient_identifier,
            content=request.content,
            response_type=request.response_type,
            priority=request.priority,
            requires_approval=request.requires_approval,
            subject=request.subject
        )

        return SendResponseResponse(
            id=result.get("id"),
            status=ResponseStatus[result.get("status", "QUEUED")],
            queued_at=result.get("queued_at", datetime.now().isoformat()),
            channel=request.channel,
            recipient=request.recipient_identifier
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending response: {str(e)}"
        )


@communication_router.get("/response-status/{response_id}", response_model=ResponseStatusResponse)
async def get_response_status(
    response_id: str,
    coordinator: ResponseCoordinator = Depends(get_response_coordinator)
):
    """
    Get the status of a specific response
    """
    try:
        status_info = coordinator.get_response_status(response_id)

        if not status_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Response with ID {response_id} not found"
            )

        return ResponseStatusResponse(
            id=response_id,
            status=ResponseStatus[status_info.get("status", "UNKNOWN")],
            timestamp=status_info.get("timestamp", datetime.now().isoformat())
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting response status: {str(e)}"
        )


@communication_router.get("/conversation/{conversation_id}", response_model=ConversationContextResponse)
async def get_conversation_context(
    conversation_id: str,
    coordinator: ResponseCoordinator = Depends(get_response_coordinator)
):
    """
    Get the context for a specific conversation
    """
    try:
        conversation_tracker = ConversationTracker(coordinator.vault_path)
        context = conversation_tracker.get_conversation_context(conversation_id)

        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation with ID {conversation_id} not found"
            )

        return ConversationContextResponse(
            id=context.get("id"),
            original_channel=context.get("original_channel"),
            original_sender=context.get("original_sender"),
            context_summary=context.get("context_summary"),
            created_at=context.get("created_at"),
            last_activity=context.get("last_activity"),
            participants=context.get("participants", []),
            message_count=context.get("message_count", 0),
            active=context.get("active", True)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting conversation context: {str(e)}"
        )


@communication_router.post("/send-direct", response_model=SendResponseResponse)
async def send_direct_response(
    request: SendResponseRequest,
    coordinator: ResponseCoordinator = Depends(get_response_coordinator)
):
    """
    Send a response directly without queuing (for immediate responses)
    """
    try:
        # Send response directly
        if request.channel == CommunicationChannel.EMAIL:
            result = await coordinator.email_handler.send_response(
                recipient_identifier=request.recipient_identifier,
                content=request.content,
                subject=request.subject or "Response from AI Employee"
            )
        elif request.channel == CommunicationChannel.LINKEDIN:
            result = await coordinator.linkedin_handler.send_response(
                recipient_identifier=request.recipient_identifier,
                content=request.content
            )
        elif request.channel == CommunicationChannel.WHATSAPP:
            result = await coordinator.whatsapp_handler.send_response(
                recipient_identifier=request.recipient_identifier,
                content=request.content
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported communication channel: {request.channel}"
            )

        return SendResponseResponse(
            id=result.get("id", f"direct_{int(datetime.now().timestamp())}"),
            status=ResponseStatus[result.get("status", "SENT")],
            queued_at=result.get("timestamp", datetime.now().isoformat()),
            channel=request.channel,
            recipient=request.recipient_identifier
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending direct response: {str(e)}"
        )


@communication_router.get("/conversations", response_model=Dict[str, Any])
async def get_active_conversations(
    coordinator: ResponseCoordinator = Depends(get_response_coordinator)
):
    """
    Get list of active conversations
    """
    try:
        conversation_tracker = ConversationTracker(coordinator.vault_path)
        # Get recent conversations (last 30 days)
        conversations = conversation_tracker.get_recent_conversations(limit=50)

        return {
            "conversations": conversations,
            "total_count": len(conversations),
            "last_updated": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting conversations: {str(e)}"
        )
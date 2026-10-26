"""
FastAPI router for ClinIQ Phase 5 Grounded AI Copilot.

Endpoints:
  POST /api/v1/ai-copilot/chat — Global & Patient-scoped AI Copilot query endpoint.
"""
from __future__ import annotations

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.modules.ai_copilot.schema import AICopilotChatRequest, AICopilotChatResponse
from app.modules.ai_copilot.service import AICopilotService
from app.shared.schemas.common import APIResponse

router = APIRouter(prefix="/ai-copilot", tags=["AI Copilot"])


@router.post(
    "/chat",
    response_model=APIResponse[AICopilotChatResponse],
    status_code=status.HTTP_200_OK,
    summary="Ask ClinIQ AI Copilot a grounded clinical question",
)
@router.post(
    "/query",
    response_model=APIResponse[AICopilotChatResponse],
    status_code=status.HTTP_200_OK,
    summary="Query ClinIQ AI Copilot (alias endpoint)",
)
async def chat_with_copilot(
    req: AICopilotChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[AICopilotChatResponse]:
    """
    Execute 12-stage Grounded RAG pipeline for a clinician query.
    Enforces JWT.sub clinician isolation and patient ownership.
    """
    clinician_id = str(current_user.get("sub") or current_user.get("id"))
    service = AICopilotService(db)
    res = await service.process_chat_message(req=req, clinician_id=clinician_id)
    return APIResponse(data=res)


@router.get(
    "/patients/{patient_id}/history",
    response_model=APIResponse[List[Dict[str, Any]]],
    summary="Get patient chat history",
)
async def get_patient_history(
    patient_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[List[Dict[str, Any]]]:
    """Retrieve historical copilot questions and answers for a specific patient."""
    clinician_id = str(current_user.get("sub") or current_user.get("id"))
    service = AICopilotService(db)
    history = await service.get_patient_chat_history(patient_id, clinician_id)
    return APIResponse(data=history)

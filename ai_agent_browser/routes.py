from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ai_agent_browser.models import (
    ChatRequest,
    ChatResponse,
    RAGQueryRequest,
    RAGQueryResponse
)
from ai_agent_browser.services import (
    pick_provider,
    provider_label,
    send_gemini_chat,
    send_openai_chat,
    perform_rag_query
)

router = APIRouter(prefix="/api/ai-agent-browser", tags=["ai-agent-browser"])

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Agent Browser FastAPI Service"
    }

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Unified AI Chat Endpoint for AI Agent Browser.
    Selects Gemini or GPT dynamically, or honors requested provider.
    """
    messages_dict = [{"role": m.role, "content": m.content} for m in req.messages]
    last_user_msg = next((m.content for m in reversed(req.messages) if m.role == 'user'), "")

    provider = req.forced_provider or pick_provider(last_user_msg, req.response_language)
    model = req.forced_model or ('gemini-1.5-flash' if provider == 'gemini' else 'gpt-4o')
    label = provider_label(provider)

    try:
        if provider == 'gemini':
            reply = await send_gemini_chat(
                messages=messages_dict,
                model=model,
                temperature=req.temperature,
                max_tokens=req.max_tokens,
                user_key=req.user_gemini_key
            )
        else:
            reply = await send_openai_chat(
                messages=messages_dict,
                model=model,
                temperature=req.temperature,
                max_tokens=req.max_tokens,
                user_key=req.user_openai_key
            )
        return ChatResponse(
            reply=reply,
            provider=provider,
            provider_label=label,
            model=model
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/rag", response_model=RAGQueryResponse)
def rag_query(req: RAGQueryRequest):
    """
    RAG Search & Retrieval Endpoint.
    """
    res = perform_rag_query(query=req.query, documents=req.documents, top_k=req.top_k)
    return RAGQueryResponse(
        answer=res["answer"],
        citations=res["citations"]
    )

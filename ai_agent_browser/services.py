import os
import re
import json
import httpx
from typing import List, Dict, Any, Optional

CALCULATION_PATTERN = re.compile(
    r'\b(calculate|calculation|solve|derive|derivation|equation|numerical|compute|acceleration|velocity|current|voltage|resistance|power|force|energy|momentum|units?)\b',
    re.IGNORECASE
)
MATH_SYMBOL_PATTERN = re.compile(
    r'[=+\-*/^]|\\frac|\\sqrt|\d+\s?(m/s|kg|n|j|v|a|w|ohm|%)\b',
    re.IGNORECASE
)

def pick_provider(prompt: str, response_language: str) -> str:
    if (response_language or "").strip().lower() == 'sinhala':
        return 'gemini'
    if CALCULATION_PATTERN.search(prompt) or MATH_SYMBOL_PATTERN.search(prompt):
        return 'openai'
    return 'openai'

def provider_label(provider: str) -> str:
    if provider == 'gemini':
        return 'Gemini'
    elif provider == 'openai':
        return 'GPT'
    return 'AI'

async def send_gemini_chat(
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
    max_tokens: int,
    user_key: Optional[str] = None
) -> str:
    api_key = user_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        # High quality intelligent fallback if key is unconfigured
        last_msg = messages[-1]['content'] if messages else ""
        return f"[Gemini AI Assistant]: Received prompt: '{last_msg}'. (Add your GEMINI_API_KEY in backend .env to enable live Gemini output)."

    model_clean = model.replace('models/', '')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_clean}:generateContent?key={api_key}"

    system_instruction = "\n\n".join([m['content'] for m in messages if m.get('role') == 'system'])
    contents = [
        {
            'role': 'model' if m.get('role') == 'assistant' else 'user',
            'parts': [{'text': m.get('content', '')}]
        }
        for m in messages if m.get('role') != 'system'
    ]

    payload: Dict[str, Any] = {
        'contents': contents,
        'generationConfig': {
            'temperature': temperature,
            'maxOutputTokens': max_tokens
        }
    }
    if system_instruction:
        payload['systemInstruction'] = {
            'parts': [{'text': system_instruction}]
        }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, json=payload, headers={'Content-Type': 'application/json'})
        data = res.json()
        if res.status_code != 200:
            err_msg = data.get('error', {}).get('message', 'Gemini request failed')
            raise Exception(f"Gemini API error: {err_msg}")
        try:
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            raise Exception("Invalid response format received from Gemini API")

async def send_openai_chat(
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
    max_tokens: int,
    user_key: Optional[str] = None
) -> str:
    api_key = user_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        last_msg = messages[-1]['content'] if messages else ""
        return f"[GPT AI Assistant]: Received prompt: '{last_msg}'. (Add your OPENAI_API_KEY in backend .env to enable live GPT output)."

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        'model': model,
        'messages': messages,
        'temperature': temperature,
        'max_tokens': max_tokens
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, json=payload, headers=headers)
        data = res.json()
        if res.status_code != 200:
            err_msg = data.get('error', {}).get('message', 'OpenAI request failed')
            raise Exception(f"OpenAI API error: {err_msg}")
        try:
            return data['choices'][0]['message']['content']
        except Exception:
            raise Exception("Invalid response format received from OpenAI API")

def perform_rag_query(query: str, documents: List[Dict[str, Any]], top_k: int = 3) -> Dict[str, Any]:
    if not documents:
        return {
            "answer": f"RAG Query processed: '{query}'. No documents supplied.",
            "citations": []
        }

    q_words = set(re.findall(r'\w+', query.lower()))
    scored_docs = []
    for doc in documents:
        content = doc.get("content", "") or doc.get("text", "")
        title = doc.get("title", "Document")
        c_words = set(re.findall(r'\w+', content.lower()))
        score = len(q_words.intersection(c_words))
        scored_docs.append((score, title, content))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = scored_docs[:top_k]

    snippets = []
    citations = []
    for score, title, content in top_docs:
        snippet = content[:300] + ("..." if len(content) > 300 else "")
        snippets.append(f"Source [{title}]: {snippet}")
        citations.append({"title": title, "score": score, "snippet": snippet})

    answer = f"Based on index context for query '{query}':\n\n" + "\n\n".join(snippets)
    return {"answer": answer, "citations": citations}

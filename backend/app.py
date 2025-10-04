"""
Personal AI Assistant API
A FastAPI backend that serves an AI chatbot representing your professional profile.
"""

import os
import json
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from prompt_template import generate_system_prompt, get_welcome_message

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Personal AI Assistant API",
    description="AI chatbot representing a professional profile for recruitment purposes",
    version="1.0.0"
)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
RATE_LIMIT = os.getenv("RATE_LIMIT", "10/minute")

# Initialize LLM client based on provider
if LLM_PROVIDER == "openai":
    from openai import OpenAI
    llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elif LLM_PROVIDER == "anthropic":
    from anthropic import Anthropic
    llm_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
else:
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")


# Pydantic models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    response: str
    timestamp: str


class WelcomeResponse(BaseModel):
    message: str


# Generate system prompt once at startup
SYSTEM_PROMPT = generate_system_prompt()


def call_openai(messages: List[dict]) -> str:
    """Call OpenAI API with the conversation history."""
    try:
        response = llm_client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")


def call_anthropic(messages: List[dict]) -> str:
    """Call Anthropic Claude API with the conversation history."""
    try:
        # Anthropic requires system message separately
        system_msg = next((msg["content"] for msg in messages if msg["role"] == "system"), "")
        conversation = [msg for msg in messages if msg["role"] != "system"]

        response = llm_client.messages.create(
            model=MODEL_NAME,
            max_tokens=300,
            system=system_msg,
            messages=conversation
        )
        return response.content[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anthropic API error: {str(e)}")


def get_llm_response(messages: List[dict]) -> str:
    """Get response from the configured LLM provider."""
    if LLM_PROVIDER == "openai":
        return call_openai(messages)
    elif LLM_PROVIDER == "anthropic":
        return call_anthropic(messages)
    else:
        raise HTTPException(status_code=500, detail="LLM provider not configured")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Personal AI Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send a message and get AI response",
            "/welcome": "GET - Get welcome message",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "provider": LLM_PROVIDER, "model": MODEL_NAME}


@app.get("/welcome", response_model=WelcomeResponse)
async def get_welcome():
    """Get the welcome message for the chat interface."""
    return WelcomeResponse(message=get_welcome_message())


@app.post("/chat", response_model=ChatResponse)
@limiter.limit(RATE_LIMIT)
async def chat(request: Request, chat_request: ChatRequest):
    """
    Main chat endpoint. Receives a message and conversation history,
    returns AI response.
    """
    try:
        # Build messages array for LLM
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history (keep last 10 messages for context)
        history = chat_request.conversation_history[-10:] if chat_request.conversation_history else []
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # Add current user message
        messages.append({"role": "user", "content": chat_request.message})

        # Get LLM response
        ai_response = get_llm_response(messages)

        return ChatResponse(
            response=ai_response,
            timestamp=datetime.utcnow().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

#!/usr/bin/env python3
"""
Startup script for the Perplexity AI Clone
"""
import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import perplexity_agent
from specialized_agents import sports_agent, finance_agent
from models import ChatRequest, ChatResponse, HealthResponse
from conversation_storage import conversation_manager

load_dotenv()

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["OPENAI_API_KEY", "SERP_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file with these variables or set them in your environment.")
        return False
    
    print("All required environment variables are set!")
    return True

app = FastAPI(
    title="Perplexity AI Clone",
    description="A Perplexity AI clone using OpenAI Agents SDK with web search capabilities",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint for health check"""
    return HealthResponse(
        status="healthy",
        message="Perplexity AI Clone is running"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is running properly"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes user messages and returns AI responses
    with web search capabilities
    """
    try:
        # Process the chat request using the agent (now async)
        result = await perplexity_agent.chat(
            message=request.message,
            thread_id=request.thread_id
        )
        
        return ChatResponse(
            response=result["response"],
            thread_id=result["thread_id"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@app.post("/chat/sports", response_model=ChatResponse)
async def chat_sports(request: ChatRequest):
    """
    Sports specialist chat endpoint that processes sports-related queries
    """
    try:
        result = await sports_agent.chat(
            message=request.message,
            thread_id=request.thread_id
        )
        
        return ChatResponse(
            response=result["response"],
            thread_id=result["thread_id"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing sports chat request: {str(e)}"
        )

@app.get("/chat/sports/summary", response_model=ChatResponse)
async def sports_initial_summary():
    """
    Get initial sports summary for the sports landing page
    """
    try:
        result = await sports_agent.get_initial_summary()
        
        return ChatResponse(
            response=result["response"],
            thread_id=result["thread_id"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating sports summary: {str(e)}"
        )

@app.post("/chat/finance", response_model=ChatResponse)
async def chat_finance(request: ChatRequest):
    """
    Finance specialist chat endpoint that processes finance-related queries
    """
    try:
        result = await finance_agent.chat(
            message=request.message,
            thread_id=request.thread_id
        )
        
        return ChatResponse(
            response=result["response"],
            thread_id=result["thread_id"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing finance chat request: {str(e)}"
        )

@app.get("/chat/finance/summary", response_model=ChatResponse)
async def finance_initial_summary():
    """
    Get initial finance summary for the finance landing page
    """
    try:
        result = await finance_agent.get_initial_summary()
        
        return ChatResponse(
            response=result["response"],
            thread_id=result["thread_id"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating finance summary: {str(e)}"
        )

@app.delete("/conversations/{thread_id}")
async def clear_conversation(thread_id: str):
    """
    Clear conversation history for a specific thread
    """
    try:
        await conversation_manager.clear_session(thread_id)
        return {"message": f"Conversation {thread_id} cleared successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing conversation: {str(e)}"
        )

@app.post("/search")
async def direct_search(query: str, num_results: int = 5):
    """
    Direct web search endpoint for testing the search functionality
    """
    try:
        from tools import execute_web_search
        results = execute_web_search(query, num_results)
        return {"query": query, "results": results}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing search: {str(e)}"
        )

@app.get("/agent/info")
async def get_agent_info():
    """Get information about the current agent"""
    try:
        agent = perplexity_agent.create_agent()
        return {
            "name": agent.name,
            "model": agent.model,
            "tools": [tool.__name__ for tool in agent.tools] if agent.tools else []
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting agent info: {str(e)}"
        )

@app.get("/agents/info")
async def get_all_agents_info():
    """Get information about all available agents"""
    try:
        general_agent = perplexity_agent.create_agent()
        sports_agent_info = sports_agent.create_agent()
        finance_agent_info = finance_agent.create_agent()
        
        return {
            "agents": [
                {
                    "type": "general",
                    "name": general_agent.name,
                    "model": general_agent.model,
                    "endpoint": "/chat",
                    "tools": [tool.__name__ for tool in general_agent.tools] if general_agent.tools else []
                },
                {
                    "type": "sports",
                    "name": sports_agent_info.name,
                    "model": sports_agent_info.model,
                    "endpoint": "/chat/sports",
                    "summary_endpoint": "/chat/sports/summary",
                    "tools": [tool.__name__ for tool in sports_agent_info.tools] if sports_agent_info.tools else []
                },
                {
                    "type": "finance",
                    "name": finance_agent_info.name,
                    "model": finance_agent_info.model,
                    "endpoint": "/chat/finance",
                    "summary_endpoint": "/chat/finance/summary",
                    "tools": [tool.__name__ for tool in finance_agent_info.tools] if finance_agent_info.tools else []
                }
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting agents info: {str(e)}"
        )

def main():
    print("Starting Perplexity AI Clone...")
    
    if not check_environment():
        return
    
    print("Starting FastAPI server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 
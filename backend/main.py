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
from models import ChatRequest, ChatResponse, HealthResponse

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
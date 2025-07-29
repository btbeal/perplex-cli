from openai import OpenAI
from agents import Agent, Runner
from dotenv import load_dotenv
import os
import logging
from models import PerplexityResponse
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
load_dotenv()


class BaseAgent(ABC):
    """Base agent class containing common functionality for all specialized agents"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agent = None
        
    @abstractmethod
    def create_agent(self):
        """Create the specialized agent - must be implemented by subclasses"""
        pass
    
    async def chat(self, message: str, thread_id: str = None):
        """Chat with the agent - common implementation for all agents"""
        if not self.agent:
            self.create_agent()
        
        try:
            result = await Runner.run(self.agent, message)
            if not thread_id:
                import uuid
                thread_id = str(uuid.uuid4())
            
            logger.info(f"{self.__class__.__name__} response: {result}")
            
            # Extract the structured response
            structured_response = result.final_output_as(PerplexityResponse)
            
            return {
                "response": structured_response,
                "thread_id": thread_id
            }
            
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__} chat: {e}")
            return {
                "response": PerplexityResponse(
                    summary=f"I encountered an error while processing your request: {str(e)}",
                    explore_more=[]
                ),
                "thread_id": thread_id or "error"
            }

    async def get_initial_summary(self):
        """Get an initial summary - can be overridden by subclasses for custom prompts"""
        return await self.chat("Give me a comprehensive overview of the latest news and updates in this domain.") 
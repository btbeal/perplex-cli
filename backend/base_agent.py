from openai import OpenAI
from agents import Agent, Runner
from dotenv import load_dotenv
import os
import logging
import uuid
from models import PerplexityResponse
from abc import ABC, abstractmethod
from conversation_storage import conversation_manager

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
        
        # Generate thread_id if not provided
        if not thread_id:
            thread_id = str(uuid.uuid4())
        
        try:
            # Get the session for this thread_id
            session = conversation_manager.get_session(thread_id)
            
            # Run the agent with session to maintain conversation history
            result = await Runner.run(
                starting_agent=self.agent,
                input=message,
                session=session
            )
            
            logger.info(f"{self.__class__.__name__} response: {result}")
            
            # Extract the structured response
            structured_response = result.final_output_as(PerplexityResponse)
            
            return {
                "response": structured_response,
                "thread_id": thread_id
            }
            
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__} chat: {e}")
            error_response = PerplexityResponse(
                summary=f"I encountered an error while processing your request: {str(e)}",
                explore_more=[]
            )
            
            return {
                "response": error_response,
                "thread_id": thread_id or "error"
            }

    async def get_initial_summary(self):
        """Get an initial summary - can be overridden by subclasses for custom prompts"""
        return await self.chat("Give me a comprehensive overview of the latest news and updates in this domain.")
    
    async def clear_conversation(self, thread_id: str):
        """Clear conversation history for a specific thread"""
        await conversation_manager.clear_session(thread_id) 
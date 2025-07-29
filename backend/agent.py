from openai import OpenAI
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import os
from tools import execute_web_search
import logging
from models import Source, PerplexityResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
load_dotenv()


@function_tool
def web_search(query: str, num_results: int = 5) -> str:
    """Search the web for current information on any topic"""
    return execute_web_search(query, num_results)

class PerplexityAgent:
    """Main agent class for the Perplexity AI clone using OpenAI Agent SDK"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agent = None
        
    def create_agent(self):
        """Create the OpenAI agent with tools"""
        if not self.agent:
            self.agent = Agent(
                name="Perplexity AI Clone",
                instructions="""You are a helpful AI assistant similar to Perplexity AI. 
                
                When users ask questions that require current information, use the web_search tool 
                to find relevant, up-to-date information and then provide your response in the 
                structured format.
                
                Your response should include:
                1. A comprehensive summary that synthesizes the search results into a clear, 
                   informative response written in a natural, engaging style
                2. A list of all sources from your search results, each with the exact title 
                   and complete URL
                
                Make sure to:
                - Write a comprehensive but concise summary
                - Include ALL sources from your search results
                - Use the exact titles and URLs provided in the search results
                - Cite specific facts and figures when available in the summary""",
                tools=[web_search],
                model="gpt-4o-mini",
                output_type=PerplexityResponse
            )
        return self.agent
    
    async def chat(self, message: str, thread_id: str = None):
        """Chat with the agent"""
        if not self.agent:
            self.create_agent()
        
        try:
            result = await Runner.run(self.agent, message)
            if not thread_id:
                import uuid
                thread_id = str(uuid.uuid4())
            
            logger.info(f"Agent response: {result}")
            
            # Extract the structured response
            structured_response = result.final_output_as(PerplexityResponse)
            
            return {
                "response": structured_response,
                "thread_id": thread_id
            }
            
        except Exception as e:
            logger.error(f"Error in agent chat: {e}")
            return {
                "response": PerplexityResponse(
                    summary=f"I encountered an error while processing your request: {str(e)}",
                    explore_more=[]
                ),
                "thread_id": thread_id or "error"
            }

# Create a global instance
perplexity_agent = PerplexityAgent()

from openai import OpenAI
from agents import function_tool
from dotenv import load_dotenv
import os
from tools import execute_web_search
import logging
from models import PerplexityResponse
from base_agent import BaseAgent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
load_dotenv()

# Create the web search tool using function_tool decorator
@function_tool
def web_search(query: str, num_results: int = 5) -> str:
    """Search the web for current information on any topic"""
    # Add subtle current context to search queries for more recent results (less aggressive)
    enhanced_query = f"{query} recent latest"
    return execute_web_search(enhanced_query, num_results)

class PerplexityAgent(BaseAgent):
    """Main agent class for the Perplexity AI clone using OpenAI Agent SDK"""
        
    def create_agent(self):
        """Create the OpenAI agent with tools"""
        if not self.agent:
            from agents import Agent
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
                - Write a comprehensive but concise summary focusing on current and recent information
                - Include ALL sources from your search results
                - Use the exact titles and URLs provided in the search results
                - Cite specific facts and figures when available in the summary
                - Prioritize recent information and current events
                - When searching, focus on the most up-to-date information available""",
                tools=[web_search],
                model="gpt-4o-mini",
                output_type=PerplexityResponse
            )
        return self.agent

# Create a global instance
perplexity_agent = PerplexityAgent()

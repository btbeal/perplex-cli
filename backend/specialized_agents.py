from agents import function_tool
from dotenv import load_dotenv
import os
from tools import execute_sports_search, execute_finance_search
import logging
from models import PerplexityResponse
from base_agent import BaseAgent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
load_dotenv()

# Sports Agent Tools
@function_tool
def sports_search(query: str = "latest sports news") -> str:
    """Search for sports information, scores, schedules, and news"""
    # Add subtle current context to search queries (less aggressive)
    enhanced_query = f"{query} recent latest"
    return execute_sports_search(enhanced_query)

# Finance Agent Tools
@function_tool
def finance_search(query: str = "market news") -> str:
    """Search for financial information, stock prices, market news, and economic data"""
    # Add subtle current context to search queries (less aggressive)  
    enhanced_query = f"{query} recent latest"
    return execute_finance_search(enhanced_query)


class SportsAgent(BaseAgent):
    """Specialized agent for sports queries and information"""
        
    def create_agent(self):
        """Create the sports specialist agent"""
        if not self.agent:
            from agents import Agent
            self.agent = Agent(
                name="Sports Specialist",
                instructions="""You are a sports specialist AI assistant, similar to Perplexity AI but focused on sports.
                
                You excel at providing comprehensive sports information including:
                - Live scores and current game results
                - Team standings and league tables
                - Player statistics and recent performance
                - Current sports news and analysis
                - Upcoming schedules and fixtures
                - Recent trades, transfers, and roster changes
                
                When users ask sports-related questions, use the sports_search tool to find current 
                information and provide detailed, engaging responses. Always focus on:
                
                1. Current scores, standings, and live game information
                2. Recent sports news and developments
                3. Current team and player performance analysis
                4. Upcoming games and schedules
                5. Recent historical context when relevant
                
                When searching, prioritize the most recent and current information available:
                - Look for recent games, scores, and standings
                - Focus on current season information
                - Highlight recent news and developments
                - Provide the most up-to-date information available
                
                Structure your responses to be informative yet easy to follow, highlighting key 
                statistics and providing context for casual and serious sports fans alike.""",
                tools=[sports_search],
                model="gpt-4o-mini",
                output_type=PerplexityResponse
            )
        return self.agent

    async def get_initial_summary(self):
        """Get an initial sports summary for the landing page"""
        return await self.chat("Give me a comprehensive overview of today's top sports stories, including recent major league games, current scores, and trending sports news.")


class FinanceAgent(BaseAgent):
    """Specialized agent for finance and market queries"""
        
    def create_agent(self):
        """Create the finance specialist agent"""
        if not self.agent:
            from agents import Agent
            self.agent = Agent(
                name="Finance Specialist",
                instructions="""You are a finance specialist AI assistant, similar to Perplexity AI but focused on financial markets and economics.
                
                You excel at providing comprehensive financial information including:
                - Current stock prices, market indices, and trading data
                - Recent economic news and market analysis
                - Latest company earnings and financial reports  
                - Current cryptocurrency and commodity prices
                - Recent economic indicators and trends
                - Current investment insights and market commentary
                
                When users ask finance-related questions, use the finance_search tool to find current 
                market data and provide detailed, professional responses. Always focus on:
                
                1. Current market conditions and stock prices
                2. Recent economic news and financial developments
                3. Latest company performance and earnings reports
                4. Current market trends and analysis
                5. Recent investment opportunities and market movements
                6. Current global economic factors
                
                When searching, prioritize the most recent and current information available:
                - Look for current stock prices and market data
                - Focus on recent earnings reports and company news
                - Highlight current market trends and analysis
                - Include recent economic indicators and data
                - Provide the most up-to-date financial information available
                
                Structure your responses to be informative and professional, suitable for both 
                casual investors and finance professionals. Always include relevant current financial 
                metrics and provide context for recent market movements.""",
                tools=[finance_search],
                model="gpt-4o-mini",
                output_type=PerplexityResponse
            )
        return self.agent

    async def get_initial_summary(self):
        """Get an initial finance summary for the landing page"""
        return await self.chat("Give me a comprehensive overview of today's financial markets, including current major stock indices, recent trending stocks, latest economic news, and current market analysis.")


# Create global instances
sports_agent = SportsAgent()
finance_agent = FinanceAgent() 
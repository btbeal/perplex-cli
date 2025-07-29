import os
from typing import Dict, Any, List
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

class WebSearchTool:
    """Tool for web search using SerpAPI"""
    
    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")
        if not self.api_key:
            raise ValueError("SERP_API_KEY environment variable is required")
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search using SerpAPI with date filtering for recent results
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "engine": "google",
                "tbs": "qdr:y",  # Filter for results from the past year (more realistic)
                "sort": "date"   # Sort by date (most recent first)
            })
            
            results = search.get_dict()
            
            # Extract organic results
            organic_results = results.get("organic_results", [])
            
            formatted_results = []
            for result in organic_results[:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "displayed_link": result.get("displayed_link", ""),
                    "date": result.get("date", "")
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error performing web search: {e}")
            return []

    def sports_search(self, query: str = "latest sports news") -> List[Dict[str, Any]]:
        """
        Perform a sports-focused search using SerpAPI with recent date filtering
        
        Args:
            query: Sports query
            
        Returns:
            List of sports results with structured data
        """
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.api_key,
                "engine": "google",
                "tbs": "qdr:m",  # Filter for results from the past month (more realistic)
                "sort": "date"   # Sort by date (most recent first)
            })
            
            results = search.get_dict()
            
            # Check for sports results first
            sports_results = results.get("sports_results", {})
            organic_results = results.get("organic_results", [])
            
            formatted_results = []
            
            # Add sports-specific results if available
            if sports_results:
                formatted_results.append({
                    "title": f"Sports: {sports_results.get('title', 'Sports Results')}",
                    "link": "https://www.google.com/search?q=" + query.replace(" ", "+"),
                    "snippet": f"Sports data: {str(sports_results)[:200]}...",
                    "displayed_link": "google.com/sports",
                    "type": "sports_data",
                    "date": "current"
                })
            
            # Add regular organic results
            for result in organic_results[:4]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "displayed_link": result.get("displayed_link", ""),
                    "type": "organic",
                    "date": result.get("date", "")
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error performing sports search: {e}")
            return []

    def finance_search(self, query: str = "market news") -> List[Dict[str, Any]]:
        """
        Perform a finance-focused search using SerpAPI with recent date filtering
        
        Args:
            query: Finance query
            
        Returns:
            List of finance results with market data
        """
        try:
            # Try Google Finance API first for stock-specific queries
            if "stock" in query.lower() or len(query.split()) <= 2:
                search = GoogleSearch({
                    "engine": "google_finance",
                    "q": query,
                    "api_key": self.api_key
                })
                
                finance_results = search.get_dict()
                
                if finance_results.get("summary") or finance_results.get("knowledge_graph"):
                    formatted_results = []
                    
                    if finance_results.get("summary"):
                        summary = finance_results["summary"]
                        formatted_results.append({
                            "title": f"Finance: {summary.get('title', 'Market Summary')}",
                            "link": "https://www.google.com/finance",
                            "snippet": f"Price: {summary.get('price', 'N/A')}, Change: {summary.get('price_change', 'N/A')}",
                            "displayed_link": "google.com/finance",
                            "type": "finance_data",
                            "date": "current"
                        })
                    
                    # Add any organic results for additional context
                    organic_results = finance_results.get("organic_results", [])
                    for result in organic_results[:3]:
                        formatted_results.append({
                            "title": result.get("title", ""),
                            "link": result.get("link", ""),
                            "snippet": result.get("snippet", ""),
                            "displayed_link": result.get("displayed_link", ""),
                            "type": "organic",
                            "date": result.get("date", "")
                        })
                    
                    return formatted_results
            
            # Fall back to regular search with finance focus and date filtering
            search = GoogleSearch({
                "q": f"finance {query} market news stock",
                "api_key": self.api_key,
                "engine": "google",
                "tbs": "qdr:w",  # Filter for results from the past week (more realistic than daily)
                "sort": "date"   # Sort by date (most recent first)
            })
            results = search.get_dict()
            organic_results = results.get("organic_results", [])
            
            formatted_results = []
            for result in organic_results[:5]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "displayed_link": result.get("displayed_link", ""),
                    "type": "organic",
                    "date": result.get("date", "")
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error performing finance search: {e}")
            return []

def get_web_search_tool_definition():
    """Return the tool definition for OpenAI Agents"""
    return {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information on any topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    }

def get_sports_search_tool_definition():
    """Return the sports search tool definition for OpenAI Agents"""
    return {
        "type": "function",
        "function": {
            "name": "sports_search",
            "description": "Search for sports information, scores, schedules, and news",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The sports search query (team names, league, sport type, etc.)",
                        "default": "latest sports news"
                    }
                },
                "required": []
            }
        }
    }

def get_finance_search_tool_definition():
    """Return the finance search tool definition for OpenAI Agents"""
    return {
        "type": "function",
        "function": {
            "name": "finance_search",
            "description": "Search for financial information, stock prices, market news, and economic data",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The finance search query (stock symbols, company names, market terms, etc.)",
                        "default": "market news"
                    }
                },
                "required": []
            }
        }
    }

# Initialize the web search tool
web_search_tool = WebSearchTool()

def execute_web_search(query: str, num_results: int = 5) -> str:
    """Execute web search and return formatted results"""
    results = web_search_tool.search(query, num_results)
    
    if not results:
        return "No search results found."
    
    formatted_output = f"Web search results for '{query}':\n\n"
    formatted_output += "=== SEARCH RESULTS ===\n\n"
    
    for i, result in enumerate(results, 1):
        formatted_output += f"Result {i}:\n"
        formatted_output += f"Title: {result['title']}\n"
        formatted_output += f"URL: {result['link']}\n"
        formatted_output += f"Content: {result['snippet']}\n"
        formatted_output += f"Source: {result['displayed_link']}\n"
        if result.get('date'):
            formatted_output += f"Date: {result['date']}\n"
        formatted_output += "\n"
    
    formatted_output += "=== END RESULTS ===\n\n"
    formatted_output += "Instructions: Use this information to create a comprehensive summary focusing on the most recent information and include ALL sources in an 'Explore More' section with titles and URLs."
    
    return formatted_output

def execute_sports_search(query: str = "latest sports news") -> str:
    """Execute sports search and return formatted results"""
    results = web_search_tool.sports_search(query)
    
    if not results:
        return "No sports results found."
    
    formatted_output = f"Sports search results for '{query}':\n\n"
    formatted_output += "=== SPORTS RESULTS ===\n\n"
    
    for i, result in enumerate(results, 1):
        formatted_output += f"Result {i}:\n"
        formatted_output += f"Title: {result['title']}\n"
        formatted_output += f"URL: {result['link']}\n"
        formatted_output += f"Content: {result['snippet']}\n"
        formatted_output += f"Source: {result['displayed_link']}\n"
        formatted_output += f"Type: {result.get('type', 'organic')}\n"
        if result.get('date'):
            formatted_output += f"Date: {result['date']}\n"
        formatted_output += "\n"
    
    formatted_output += "=== END RESULTS ===\n\n"
    formatted_output += "Instructions: Use this sports information to create a comprehensive summary focusing on current games, recent scores, schedules, and sports news. Include ALL sources in an 'Explore More' section."
    
    return formatted_output

def execute_finance_search(query: str = "market news") -> str:
    """Execute finance search and return formatted results"""
    results = web_search_tool.finance_search(query)
    
    if not results:
        return "No finance results found."
    
    formatted_output = f"Finance search results for '{query}':\n\n"
    formatted_output += "=== FINANCE RESULTS ===\n\n"
    
    for i, result in enumerate(results, 1):
        formatted_output += f"Result {i}:\n"
        formatted_output += f"Title: {result['title']}\n"
        formatted_output += f"URL: {result['link']}\n"
        formatted_output += f"Content: {result['snippet']}\n"
        formatted_output += f"Source: {result['displayed_link']}\n"
        formatted_output += f"Type: {result.get('type', 'organic')}\n"
        if result.get('date'):
            formatted_output += f"Date: {result['date']}\n"
        formatted_output += "\n"
    
    formatted_output += "=== END RESULTS ===\n\n"
    formatted_output += "Instructions: Use this financial information to create a comprehensive summary focusing on current market trends, recent stock prices, economic news, and financial analysis. Include ALL sources in an 'Explore More' section."
    
    return formatted_output 
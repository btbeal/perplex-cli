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
        Perform a web search using SerpAPI
        
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
                "engine": "google"
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
                    "displayed_link": result.get("displayed_link", "")
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error performing web search: {e}")
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
        formatted_output += f"Source: {result['displayed_link']}\n\n"
    
    formatted_output += "=== END RESULTS ===\n\n"
    formatted_output += "Instructions: Use this information to create a comprehensive summary and include ALL sources in an 'Explore More' section with titles and URLs."
    
    return formatted_output 
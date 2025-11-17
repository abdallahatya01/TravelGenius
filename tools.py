from crewai.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from config import TAVILY_API_KEY

@tool
def web_search_tool(query: str) -> str:
    """Search for current travel information, prices, and recommendations"""
    tavily_tool = TavilySearchResults(
        max_results=5, 
        api_key=TAVILY_API_KEY,
        include_answer=True,
        include_raw_content=True
    )
    
    results = tavily_tool.invoke(query)
    
    formatted = ""
    for i, res in enumerate(results, 1):
        formatted += f"Source {i}:\n"
        formatted += f"Title: {res.get('title', 'N/A')}\n"
        formatted += f"URL: {res.get('url', 'N/A')}\n"
        formatted += f"Content: {res.get('content', res.get('snippet', 'N/A'))}\n"
        formatted += "-" * 50 + "\n\n"
    
    return formatted if formatted else "No results found."


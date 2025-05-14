import requests
import time
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search the web using SerpAPI and return the top results.
    
    Args:
        query (str): The search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict]: List of dictionaries containing search results
    """
    try:
        # Use Google search through SerpAPI
        params = {
            'engine': 'google',
            'q': query,
            'api_key': os.getenv('SERPAPI_KEY', 'demo'),  # Use demo key if not provided
            'num': max_results
        }
        
        response = requests.get('https://serpapi.com/search', params=params)
        response.raise_for_status()
        data = response.json()
        
        # Format results
        formatted_results = []
        if 'organic_results' in data:
            for result in data['organic_results'][:max_results]:
                formatted_results.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', '')
                })
        
        return formatted_results
            
    except Exception as e:
        print(f"Error during web search: {str(e)}")
        return [] 
import os
import requests
from typing import List, Tuple, Dict
import json

SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on provided web content.
Always cite your sources using [1], [2], etc. format.
Only use information from the provided sources.
If you're unsure, say so.
Format your response in markdown."""

def get_llm_response(question: str, texts: List[str], search_results: List[Dict]) -> Tuple[str, List[Dict]]:
    """
    Get response from LLM with citations.
    
    Args:
        question (str): User's question
        texts (List[str]): List of extracted texts from web pages
        search_results (List[Dict]): Original search results with metadata
        
    Returns:
        Tuple[str, List[Dict]]: Formatted answer with citations and list of sources
    """
    # Format sources for the prompt
    formatted_sources = []
    for i, (text, result) in enumerate(zip(texts, search_results), 1):
        if text:  # Only include sources that have content
            # Truncate text to reduce token usage
            formatted_sources.append(f"[{i}] {text[:500]}...")  # Reduced from 1000 to 500
    
    if not formatted_sources:
        return "I couldn't extract any meaningful content from the search results. Please try rephrasing your question.", []
    
    # Create the prompt
    user_prompt = f"""Question: {question}

Sources:
{chr(10).join(formatted_sources)}

Please provide a concise answer with citations."""

    try:
        # Prepare the request
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Ask the Web",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "openai/gpt-4",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500  # Reduced from 1000 to 500
        }
        
        # Make the request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        
        # Print response for debugging
        print("OpenRouter Response:", json.dumps(response_data, indent=2))
        
        # Check for credit limit error
        if 'error' in response_data:
            error_msg = response_data['error'].get('message', 'Unknown error')
            if 'credits' in error_msg.lower():
                return "I apologize, but I've reached my usage limit. Please try again later or upgrade your account.", []
            raise ValueError(f"API Error: {error_msg}")
        
        # Validate response structure
        if 'choices' not in response_data:
            raise ValueError("Invalid response format: missing choices")
            
        if not response_data['choices']:
            raise ValueError("Invalid response format: empty choices")
            
        if 'message' not in response_data['choices'][0]:
            raise ValueError("Invalid response format: missing message")
            
        if 'content' not in response_data['choices'][0]['message']:
            raise ValueError("Invalid response format: missing content")
        
        answer = response_data['choices'][0]['message']['content']
        
        # Format sources for display
        sources = []
        for i, result in enumerate(search_results, 1):
            sources.append({
                "id": i,
                "title": result["title"],
                "url": result["link"]
            })
        
        return answer, sources
        
    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")
        return "Sorry, I encountered a network error while processing your question.", []
    except ValueError as e:
        print(f"Response parsing error: {str(e)}")
        return "Sorry, I encountered an error while processing the response.", []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return "Sorry, I encountered an unexpected error while processing your question.", [] 
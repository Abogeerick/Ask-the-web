from newspaper import Article
import time
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import random

def extract_text_from_urls(urls: List[str], search_results: List[Dict], timeout: int = 10) -> List[str]:
    """
    Extract main text content from a list of URLs.
    
    Args:
        urls (List[str]): List of URLs to extract text from
        search_results (List[Dict]): Original search results with snippets
        timeout (int): Request timeout in seconds
        
    Returns:
        List[str]: List of extracted text content
    """
    extracted_texts = []
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    
    for i, url in enumerate(urls):
        try:
            # First try with newspaper3k
            article = Article(url)
            article.headers = {'User-Agent': random.choice(user_agents)}
            article.download()
            article.parse()
            
            if article.text:
                extracted_texts.append(article.text)
                continue
                
            # Fallback to BeautifulSoup if newspaper3k fails
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            if text:
                extracted_texts.append(text)
            else:
                # If no text found, use the snippet from search results
                snippet = search_results[i].get('snippet', '')
                extracted_texts.append(snippet if snippet else "")
            
        except Exception as e:
            print(f"Error extracting text from {url}: {str(e)}")
            # Use the snippet from search results as fallback
            snippet = search_results[i].get('snippet', '')
            extracted_texts.append(snippet if snippet else "")
            
        # Be nice to servers
        time.sleep(1)
        
    return extracted_texts 
# utils/get_web_search.py

import requests
from bs4 import BeautifulSoup

def get_duckduckgo_links(query, count=3):
    """
    Fetches the top relevant search result links from DuckDuckGo HTML page for a given query,
    limited to the specified count.

    Parameters:
    - query (str): The search query string.
    - count (int): The maximum number of results to return (default is 3).

    Returns:
    - str: A formatted string of the top search result links as markdown links.
    """
    # Prepare URL for DuckDuckGo HTML search page
    url = f"https://html.duckduckgo.com/html/?q={query}"
    
    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        # Request the HTML content of the search results page with headers
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an error for bad responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate result containers
        results = soup.select("a.result__a")
        
        # Collect formatted links, limited to the specified count
        links = []
        for i, result in enumerate(results):
            if i >= count:
                break
            title = result.get_text(strip=True)
            url = result['href']
            links.append(f"- [{title}]({url})")
                
        # If no links were found, provide a fallback message
        if not links:
            return "No relevant links found for your query."
        
        return "\n".join(links)
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching web search data: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
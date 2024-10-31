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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    
    try:
        # Request the HTML content of the search results page with headers
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an error for bad responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate result containers
        results = soup.select("div.result__body")  # Class of each search result
        
        # Collect formatted links, limited to the specified count
        links = []
        for i, result in enumerate(results):
            if i >= count:  # Stop if we reach the count limit
                break
            title_tag = result.select_one("h2.result__title a.result__a")
            url_tag = result.select_one("a.result__a")
            if title_tag and url_tag:
                title = title_tag.get_text(strip=True)
                url = url_tag['href']
                links.append(f"- [{title}]({url})")
                
        # If no links were found, provide a fallback message
        if not links:
            return "No relevant links found for your query."
        
        return "\n".join(links)
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Run the function if the script is executed directly
if __name__ == "__main__":
    query = input("Enter search query: ")
    print(get_duckduckgo_links(query))